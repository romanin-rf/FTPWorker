# FTPWorker
## Описание
Модуль **FTPWorker** сделан для упрощения работы с `ftplib`.
## Пример
- `main.py`
```python
import ftpworker

ftpw = ftpworker.FTPWorker("ftp.example.com", 21, "user", "password")
ftpw.connect()

print(ftpw.dir())

print(ftpw.dir(full_info=False))

ftpw.disconnect()
```
- Вывод
```python
[
    {
        "name": ".",
        "type": "directory",
        "size": 1024,
        "user": "user",
        "permissions": (7, 7, 7),
        "change_time": datetime(2022, 3, 19, 0, 0, 0)
    },
    {
        "name": "..",
        "type": "directory",
        "size": 1024,
        "user": "user",
        "permissions": (7, 7, 7),
        "change_time": datetime(2022, 3, 19, 0, 0, 0)
    },
    {
        "name": "example.txt",
        "type": "file",
        "size": 1024,
        "user": "user",
        "permissions": (7, 7, 7),
        "change_time": datetime(2022, 3, 19, 0, 0, 0)
    },
]

[".", "..", "example.txt"]
```
## Авторы
- `Роман Слабицкий`
    - [VK](https://vk.com/romanin2)
    - [GitHub](https://github.com/romanin-rf)