import speech_recognition as sr
from gtts import gTTS
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
import tempfile
import socket
import subprocess
import sys
import pygame
#######################################
language = "en" #'en' english or 'tr' turkish !compulsory
#######################################
__intt__ = input('Voice(ses) or (write)yazı :')
#######################################
bot = telebot.TeleBot('') # Telgram bot token !compulsory
#######################################
chat_id = '' # Telegram chat id !compulsory
#######################################
language = language.replace(' ','')
#######################################
if __intt__.lower() == 'voice' or __intt__.lower() == 'ses':
    __intt__ = 'ses'
elif __intt__.lower() == 'write' or __intt__.lower() == 'yazı':
    __intt__ = 'yazı'
else:
    print('Wrong input, try again \nYanlış giriş tekrar deneyin')
    sys.exit()
    
#######################################
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

def Cevap(message_tr,message_en):

    if language == "tr":
        speak(message_tr)
    else :
        speak(message_en)

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

def soru(message_tr,message_en):
    global command
    if language == 'tr':
        message = message_tr
        if __intt__ == 'ses':
            with sr.Microphone() as source:
                speak(f'{message}')
                audio = r.listen(source)    
                command = r.recognize_google(audio, language=language)
                print("understood command: " + command)
        elif __intt__ == 'yazı':
            speak(f'{message}')
            command = input(message+' :')
    else:
        message = message_en
        if __intt__ == 'ses':
            with sr.Microphone() as source:
                speak(f'{message}')
                audio = r.listen(source)    
                command = r.recognize_google(audio, language=language)
                print("understood command: " + command)
        elif __intt__ == 'yazı':
            speak(f'{message}')
            command = input(message+' :')


while True:
    try:
        if __intt__ == 'ses':
            with sr.Microphone() as source:
                audio = r.listen(source)    
                command = r.recognize_google(audio, language=language)
                print("understood command: " + command)
        elif __intt__ == 'yazı':
            command = input(' :')
        
        command = command.lower()

        if "plüton" in command or "pluto" in command:
            soru('Senin için ne yapmamı istersin efendim?','What do you want me to do for you, sir?')

            while True:
                try:
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
                    elif "close pluto" in command or "plüton kapan" in command:
                        Cevap('Tamamdır efendim.','Okey sir.')
                        break
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
                        Cevap("Geçersiz komut.","Invalid command.")
                except sr.UnknownValueError:
                    print("Komut anlaşılamadı.\n\nCommand not understood.")
                    break

                soru('Başka ne yapmamı istersin?','What else do you want me to do?')
    except sr.UnknownValueError:
        error = 1