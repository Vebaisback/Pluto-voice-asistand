import socket
import telebot
#######################################
language = "en" #'en' english or 'tr' turkish !compulsory
#######################################
default = 'ip'  # type "ip/Telegram" required to connect !compulsory (i prefer ip telegram not working XD)
#######################################
bot = telebot.TeleBot('') # Telgram bot token (client bot only default = 'Telegram')
#######################################
chat_id = '' # Telegram chat id !compulsory
#######################################
language = language.replace(' ','')
default = default.replace(' ','')
#######################################
if default == 'ip':

    def get_local_ip():
        try:
            #IP adresini al / get IP
            local_ip = socket.gethostbyname(socket.gethostname())
            return local_ip
        except socket.gaierror:
            return None

    HOST = get_local_ip()
    PORT = 12345

    # TCP/IP soketi oluştur / Crate socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Sunucuya bağlan / Connect server
    client_socket.connect((HOST, PORT))

#######################################

def soru(message):
    global command

    if language == 'tr':
        print("Anlaşılan komut: " + command)
    else :
        print("Agreed command: " + command)

    if default == 'Telegram':
        bot.send_message(chat_id, '/-- ' + command)
    elif default == 'ip':
        command = command.encode()
        client_socket.sendall(command)

while True:
    try:
        if default == 'Telegram':
            soru('')
            if command.startswith('/***'):
                command = command.replace('/*** ', '')
                speak(command)
        
        elif default == 'ip':

            # Veriyi sunucuya gönder / Send data to server

            soru('')

            cevap = client_socket.recv(1024).decode()
            if cevap == 'Geçersiz komut.' or cevap == 'Invalid command.':
                print(cevap)
            else:
                print('Incoming response:'+cevap)    
    except sr.UnknownValueError:
        error = 1