import telebot
import speech_recognition as sr
import pyautogui
import os
import cv2
import time
import webbrowser
import numpy as np
from bs4 import BeautifulSoup
from transformers import T5ForConditionalGeneration, T5Tokenizer
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer
import requests
import socket
import subprocess
#######################################
language = "en" #'en' english or 'tr' turkish !compulsory
#######################################
default = 'ip'  # type "ip/Telegram" required to connect !compulsory (i prefer ip telegram not working XD)
#######################################
bot = telebot.TeleBot('') # Telgram bot token (server token) !compulsory
#######################################
chat_id = '' # Telegram chat id !compulsory
#######################################
language = language.replace(' ','')
default = default.replace(' ','')
#######################################

if default == 'ip':
    def get_local_ip():
        try:
            local_ip = socket.gethostbyname(socket.gethostname())
            return local_ip
        except socket.gaierror:
            return None
    
    HOST = get_local_ip()
    PORT = 12345

def Cevap_ver(soru, uzunluk):
    url = f"https://duckduckgo.com/html/?q={soru}"
    headers = {
        "User-Agent":
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36"
    }
    yanit = ""
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        cevap = soup.find("div", class_="result__body").text
        if cevap:
            ######################
            if language == 'tr':
                tokenn = "turkish"
            else:
                tokenn = "english"
            ######################
            parser = PlaintextParser.from_string(cevap, Tokenizer(f'{tokenn}'))
            if uzunluk != 0:
                summarizer = LsaSummarizer()
                ozet = summarizer(parser.document, uzunluk)
                ozet_metin = ""
                for cumle in ozet:
                    ozet_metin += str(cumle) + " "
                yanit = ozet_metin
            else:
                ozet_metin = ""
                for cumle in parser.document.sentences:
                    ozet_metin += str(cumle) + " "
                yanit = ozet_metin
        else:
            if language == 'tr':
                yanit = "Cevap bulunamadı."
            else:
                yanit = "no answer found."
    else:
        if language == 'tr':
            yanit = "İnternet bağlantısı hatası."
        else:
            yanit ='Internet connection error.'

    return yanit

r = sr.Recognizer()

screen_width, screen_height = pyautogui.size()

def Cevap(message_tr,message_en):
    if default == 'ip':
        global command
        if language == "tr":
            command = message_tr
        else :
            command = message_en
    elif default =='Telegram':
        bot.send_message( chat_id ,'/*** '+ message)
    else:
        print('Hata')

def run_(command):
    subprocess.Popen(['start', 'cmd', '/k', command], shell=True)

def link_goster(ad):
    
    social_media = {
        'Twitter': 'www.twitter.com',
        'Instagram': 'www.instagram.com',
        'Facebook': 'www.facebook.com',
        'Telegram': 'www.telegram.org',
        'chat': 'chat.openai.com',
    }

    if ad in social_media:
        result = social_media[ad]
    else:
        result = None

    if result is None:
        print("Belirtilen sosyal medya adı bulunamadı.\n\nThe specified social media name could not be found.")
    else:
        Cevap('İstediğiniz site açıldı','The site you requested has been opened')
        subprocess.Popen(['C:/Program Files/Google/Chrome/Application/chrome.exe', result])

#######################################
def codd(commandd):
        command = commandd.lower()
        if "take ss" in command or "ss al" in command:
            Cevap('SS Telegram üzerinden atıldı','Sent via SS telegram')
            screenshot = pyautogui.screenshot()
            save_path = os.path.join("c:\\ekranss", "ss.png")
            screenshot.save(save_path)
            recipient = chat_id  
            bot.send_photo(recipient, open(save_path, 'rb'))
            os.remove(save_path)
        elif "open website" in command or "sitesini aç" in command:
            command = command.replace('open website','')
            command = command.replace('sitesini aç','')
            command = command.replace(' ', '')
            Cevap(command+ 'sistesi açılıyor',command+ 'opening website')
            link_goster(command)
        elif "do some research" in command or "kısa bir araştırma yap" in command:
            command = command.replace('do some research','')
            command = command.replace('kısa bir araştırma yap','')
            cevapd = Cevap_ver(command, 1)
            print(cevapd)
            Cevap(cevapd,cevapd)
        elif "do a long research" in command or "uzun bir araştırma yap" in command:
            command = command.replace('do a long research','')
            command = command.replace('uzun bir araştırma yap','')
            cevapd = Cevap_ver(command, 0)
            print(cevapd)
            Cevap(cevapd,cevapd)
        elif "record screen" in command or "ekranı kaydet" in command:
            # Ekran çözünürlüğü / screen resolution
            screen_width, screen_height = pyautogui.size()
            # Video codec ve dosya adı / Video codec and filename
            codec = cv2.VideoWriter_fourcc(*"XVID")
            filename = f"video.avi"
            # Video kaydedici oluştur / Crate video recorder
            video_writer = cv2.VideoWriter(filename, codec, 20.0, (screen_width, screen_height))
            # Kaydetme süreci / Saving process
            start_time = time.time()
            while time.time() - start_time < 3:  # 3 saniye kaydediyoruz / record 3 seconds
                # Ekran görüntüsünü al / Take screenshot
                screenshot = pyautogui.screenshot()
                # Ekran görüntüsünü video dosyasına yaz / Write screenshot to video file
                frame = np.array(screenshot)
                frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
                video_writer.write(frame)
            # Kaydediciyi kapat / Close recorder
            video_writer.release()
            # Video kaydedildi mesajını gönder / Send video recorded message
            Cevap('video kaydedildi','video recorded')
            
            video_path = filename  
            recipient = chat_id 
            bot.send_video(recipient, video=open(video_path, 'rb'))
            os.remove(video_path)
        else:
            Cevap("Geçersiz komut. \n\nInvalid command.")

#######################################

if default == 'Telegram':
    @bot.message_handler(func=lambda message: True)
    def handle_all_messages(message):
        if '/-- ' in message.text:
            command = message.text.replace('/-- ', '')
            codd(command)
if default == 'ip':   
    while True:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
            # Sunucuyu belirtilen HOST ve PORT'ta dinlemeye başla
            server_socket.bind((HOST, PORT))
            server_socket.listen()
            if language == 'tr':
                print(f"Sunucu dinleniyor: {HOST}:{PORT}")
            else:
                print(f"The server is listening: {HOST}:{PORT}")
            
            while True:
                # İstemci bağlantılarını kabul et
                client_socket, client_address = server_socket.accept()
                if language == 'tr':
                    print(f"İstemci bağlandı: {client_address[0]}:{client_address[1]}")
                else:
                    print(f"Client connected: {client_address[0]}:{client_address[1]}")

                while True:

                    # İstemciden gelen veriyi al
                    data = client_socket.recv(1024).decode()
                    if not data:
                        break

                    codd(data)
                    
                    # İstemciye yanıt gönder
                    response = command
                    client_socket.sendall(response.encode())
                
                # İstemci bağlantısını kapat
                client_socket.close()
        if default != 'ip':
            break