import os
from ftplib import FTP
from typing import Any, Union
from dateutil import parser as DateParser

class __info__:
	name = "FTPWorker"
	version = ("2.0-release", 2.0)
	authors = ["Роман Слабицкий"]

class __classes__:
	class Cache():
		def __init__(self) -> None:
			self.cache_data = b""
		
		def add_data(self, data: bytes) -> None:
			self.cache_data += data
		
		def delect_data(self) -> None:
			self.cache_data = b""
		
		def get_data(self) -> bytes:
			return self.cache_data
	
	class Permissions():
		def __init__(self, t: str, o: int, g: int, a: int) -> None:
			self.owner = o
			self.g = g
			self.all = a
			self.tp = t
			self.__doc__ = f"Permissions(owner={o}, groups={g}, all={a}, tp='{t}')"
		
		def get_perm(self) -> None:
			return (self.owner, self.g, self.all)

class __func__:
	def permissions_handler(perm: str) -> __classes__.Permissions:
		perml, t = [0, 0, 0], ("file" if (perm[0] == "-") else "directory")
		idx, rng = 0, 0
		for i in perm[1:]:
			if rng == 3:
				rng = 0
				idx += 1
			if i == "r":
				perml[idx] += 4
			elif i == "w":
				perml[idx] += 2
			elif i == "x":
				perml[idx] += 1
			rng += 1
		return __classes__.Permissions(t, *perml)
	
	def list_removes(l: list, data: Any) -> list:
		c = l.count(data)
		while c != 0:
			l.remove(data)
			c -= 1
		return l

	def ls_handler(data: bytes) -> None:
		# Создание и нормализация переменых
		dl, l = [i.split(" ") for i in data.decode().split("\r\n")[:-1]], []
		# Приобразование данных
		for idx, i in enumerate(dl):
			dl[idx] = __func__.list_removes(i, "")
		# Обработка
		for i in dl:
			perm = __func__.permissions_handler(i[0])
			date = DateParser.parser().parse(timestr=" ".join(i[5:8]))
			l.append(
				{
					"name": i[-1:][0],
					"type": perm.tp,
					"size": int(i[4]),
					"user": i[2],
					"permissions": perm.get_perm(),
					"change_time": date
				}
			)
		return l

class FTPWorker():
	def __init__(self, host: str, port: int=21, username: str=None, password: str=None) -> None:
		self.host = host
		self.port = port
		self.username = username
		self.password = password
		self.ftp = FTP(self.host)
		self.ftp.port = self.port

	def connect(self) -> None:
		self.ftp.login(
			user='anonymous' if (self.username is None) else self.username,
			passwd='' if (self.password is None) else self.password
		)
	
	def dir(self, full_info: bool=True) -> Union[list[dict[str, Any]], list[str]]:
		cache = __classes__.Cache()
		self.ftp.retrbinary("LIST", cache.add_data)
		return (__func__.ls_handler(cache.get_data())) if (full_info) else ([i["name"] for i in __func__.ls_handler(cache.get_data())])
	
	def cwd(self, dirname: str) -> None:
		self.ftp.cwd(dirname)

	def pwd(self) -> str:
		return self.ftp.pwd()
	
	def size(self, filename: str) -> Union[int, None]:
		return self.ftp.size(filename)
	
	def rename(self, from_name: str, to_name: str) -> None:
		self.ftp.rename(from_name, to_name)
	
	def rmd(self, dirname: str) -> None:
		self.ftp.rmd(dirname)
	
	def delete(self, filename: str) -> None:
		self.ftp.delete(filename)
	
	def download_file(self, filepath: str) -> bytes:
		cache = __classes__.Cache()
		self.ftp.retrbinary(f"RETR {filepath}", cache.add_data)
		return cache.get_data()
	
	def upload_file(self, filepath: str, *, block_size: int=1024) -> None:
		with open(filepath, "rb") as file:
			self.ftp.storbinary("STOR " + os.path.basename(filepath), file, block_size)
	
	def disconnect(self) -> None:
		self.ftp.close()