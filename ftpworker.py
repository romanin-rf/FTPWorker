from ftplib import FTP
from ftplib import FTP_TLS
import os

class FTPWorker():
	def __init__(self, host: str, *, port = 21, user = None, password = None):
		if port != 21:
			self.ftp = FTP()
			self.ftp.connect(host, port)
			if (user != None) and (password != None):
				self.ftp.login(user, password)
		else:
			self.ftp = FTP(host)
			if (user != None) and (password != None):
				self.ftp.login(user, password)

	def ls(self):
		return self.ftp.retrlines('LIST')

	def size(self, path: str):
		return self.ftp.size(path)

	def cd(self, directory = None):
		if (directory != None):
			return self.ftp.cwd(directory)
		else:
			return self.ftp.pwd()

	def delete_file(self, path: str):
		return self.ftp.delete(path)

	def delect_dir(self, path: str):
		return self.ftp.pwd(path)

	def mkdir(self, path: str):
		return self.ftp.mkd(path)

	def download_file(self, filename_in_server: str, filename_in_client: str, *, size_block = 1024):
		with open(filename_in_client, "wb") as file:
			return self.ftp.retrbinary('RETR ' + filename_in_server, file.write, 1024)

	def upload_file(self, filename_in_client: str, filename_in_server: str):
		with open(filename_in_client, "rb") as file:
			return self.ftp.storbinary('STOR ' + filename_in_server, file)

	def quit():
		return self.ftp.quit()

	def close():
		return self.ftp.close()

		