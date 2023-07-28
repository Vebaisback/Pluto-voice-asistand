import speech_recognition as sr
import telebot
import socket
import telegram
from gtts import gTTS
import tempfile
import pygame
import os
import sys

#######################################
language = "en" #'en' english or 'tr' turkish !compulsory
#######################################
__intt__ = input('Voice(ses) or (write)yazı :')
#######################################
default = 'ip'  # type "ip/Telegram" required to connect !compulsory (i prefer ip telegram not working XD)
#######################################
bot = telebot.TeleBot('') # Telegram bot token (client bot only default = 'Telegram')
#######################################
chat_id = '' # Telegram chat id !compulsory
#######################################
language = language.replace(' ','')
default = default.replace(' ','')
#######################################
if __intt__.lower() == 'voice' or __intt__.lower() == 'ses':
    __intt__ = 'ses'
elif __intt__.lower() == 'write' or __intt__.lower() == 'yazı':
    __intt__ = 'yazı'
else:
    print('Wrong input, try again \nYanlış giriş tekrar deneyin')
    sys.exit()
    
#######################################
if default == 'ip':

    def get_local_ip():
        try:
            # IP adresini al / get IP
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
r = sr.Recognizer()

def speak(message):

    tts = gTTS(text=message, lang=language, slow=False)

    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        temp_filename = temp_file.name
        tts.save(temp_filename)

    pygame.mixer.init()
    pygame.mixer.music.load(temp_filename)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        continue

    pygame.mixer.music.stop()
    pygame.mixer.quit()

    os.remove(temp_filename)

def soru(message):
    global command
    if __intt__ == 'ses':
        with sr.Microphone() as source:
            if message != '':
                speak(message)
            audio = r.listen(source)
            if language == 'tr':
                ddpd = "tr-TR"
            else :
                ddpd = "en-EN"

            command = r.recognize_google(audio, language=ddpd)
            
            if language == 'tr':
                print("Anlaşılan komut: " + command)
            else :
                print("Agreed command: " + command)
            
    elif __intt__ == 'yazı':
        command = input(message + ':')
        
        if language == 'tr':
            print("Anlaşılan komut: " + command)
        else :
            print("Agreed command: " + command)

    if default == 'Telegram':
        bot.send_message(chat_id , '/--- ' + command)
    elif default == 'ip':
        client_socket.sendall(command.encode())

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
                speak(cevap)    
    except sr.UnknownValueError:
        error = 1