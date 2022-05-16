# Spammer4Mail
Небольшой многопоточный спамер, ориентированный на работу с электронной почтой.

## Особенности
* Многопоточность
* Работа с любым SMTP
* Высокая скорость спама

## Установка
```python
pip3 install -r requirements.txt
```

## Использование
1. Данные учётных записей используемых SMTP-серверов загрузить в соответствующий конфиг-файл (по-умолчанию: __config.ini__). Пример:
```ini
[vk_group]
SMTP		= smtp.mail.ru:25
MAIL_FROM	= user@mail.ru
MAIL_PASSWORD	= 1234567890

[google]
SMTP		= smtp.gmail.com:587
MAIL_FROM	= user@gmail.com
MAIL_PASSWORD	= password
```

2. Запустить утилиту, передав следующие параметры:
```python
python Spammer4Mail.py "config.ini" "Title" "Message" "target@email.com"
```
Либо же запустить скрипт без дополнительных ключей и следовать дальнейшим подсказкам
```python
python Spammer4Mail.py
```
