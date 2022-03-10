# @base1707/Spammer4Mail
Небольшой многопоточный спамер, ориентированный на работу с электронной почтой.

## Особенности
* Многопоточность
* Работа с любым SMTP
* Высокая скорость спама

## Использование
1. Добавить используемые SMTP-сервера в .ini-файл, пример:
```ini
[vk_group]
SMTP 			= smtp.mail.ru:25
MAIL_FROM 		= user@mail.ru
MAIL_PASSWORD 	= 1234567890

[google]
SMTP 			= smtp.gmail.com:587
MAIL_FROM 		= user@gmail.com
MAIL_PASSWORD 	= password
```

2. Запустить утилиту
```python
Spammer4Mail.py "PATH_TO_CONFIG.INI" "TITLE" "MESSAGE" "TARGET@EMAIL.COM"
```