import os
from email import message
from dataclasses import replace
from unittest import result
from winreg import QueryReflectionKey
from bs4 import BeautifulSoup
import pyttsx3
import speech_recognition as sr
import pywhatkit as py
import keyboard as kb
import webbrowser
import datetime
import wikipedia
from googletrans import Translator
import requests
import bs4
import speedtest
from pywikihow import search_wikihow
import pyautogui
import psutil
import pytube
from pytube import YouTube
import time
import pyperclip
import wolframalpha
import cv2

engine = pyttsx3.init("sapi5")
voices = engine.getProperty("voices")
engine.setProperty("voice",voices[0].id)
engine.setProperty("rate",201)

def Speak(audio):
    print("   ")
    print(f":) {audio}")
    print("   ")
    engine.say(audio)
    engine.runAndWait()
   
def TakeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print(":) Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
        print(":) Recognizing...")    
        query = r.recognize_google(audio,language="en-in")
        print(f":) Your Command : {query}")
    except:
        return "None"
    return query.lower() 

def TakeCommandHindi():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print(":) Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
        print(":) Recognizing...")    
        query = r.recognize_google(audio,language="hi")
        print(f":) Your Command : {query}")
    except:
        return "None"
    return query.lower()    

def translate():
    Speak("OK, Tell me the text to translate")
    line = TakeCommandHindi()
    translator = Translator()
    result = translator.translate(line)
    Text = result.text
    Speak(Text)
    while True:
        Speak("Do you wat to translate more sentences ?")
        answer = TakeCommand()
        if answer == "close translator":
            Speak("OK, closing translator")
            break
        elif "yes" in query:
            Speak("OK, Tell me the text to translate")
            line = TakeCommandHindi()
            translator = Translator()
            result = translator.translate(line)
            Text = result.text
            Speak(Text)

def temperature():
    search = "Temperature in pune"
    url = f"https://www.google.com/search?q={search}"
    r = requests.get(url)
    data = BeautifulSoup(r.text,"html.parser")
    temp = data.find("div",class_="BNeawe").text
    Speak(f"The temperature is : {temp}")

def SpeedTest():
    Speak("Hold on, checking your internet speed")
    speed = speedtest.Speedtest()
    downloading = speed.download()
    download_speed = int(downloading/800000)
    uploading = speed.upload()
    upload_speed = int(uploading/800000)
    Speak(f"The download speed is {download_speed} megabits per second and the uploading speed is {upload_speed} megabits per second")

def date():
    from datetime import date
    today = date.today()	
    d = today.strftime("%B %d, %Y")
    Speak(f"Todays date is {d}")  

def note():
    Speak("Allright I am ready to write")
    data = TakeCommand()
    time = datetime.datetime.now().strftime("%H:%M")
    filename = time.replace(":","-") + "-note.txt"

    with open(filename,"w") as file:
        file.write(data)

    path_1 = f"E:\\Programming\\AI ASSISTANT\\{filename}"
    path_2 = f"E:\\Programming\\AI ASSISTANT\\Database\\notes\\{filename}"
    os.rename(path_1,path_2)
    os.startfile(path_2)

def YouTube_Download(link):
    url = pytube.YouTube(link)
    video = url.streams.get_highest_resolution()
    video.download("E:\\Programming\\AI ASSISTANT\\Database\\Youtube")

def close_notepad():
    os.system("TASKKILL /F /im Notepad.exe")
    Speak("File closed")

def Wolfram(query):
    api_key = "AYQ232-4TQWETHGXG"
    requester = wolframalpha.Client(api_key)
    requested = requester.query(query)

    try:
        answer = next(requested.results).text
        return answer

    except:
        Speak("Anser not found in database")

def Calculator(query):
    Term = str(query)

    Term = Term.replace("multiply","*")
    Term = Term.replace("multiplied by","*")
    Term = Term.replace("into","*")
    Term = Term.replace("plus","+")
    Term = Term.replace("minus","-")
    Term = Term.replace("plus","+")
    Term = Term.replace("by","/")
    Term = Term.replace("devided by","/")
    Term = Term.replace("upon","/")

    try:
        result = Wolfram(Term)
        Speak(result)
    except:
        Speak("Error while calculating, please try again")

def temp_any(query):
    result = Wolfram(query)
    Speak(f"{query} is : {result}")


    
if __name__=="__main__":
    Speak("Hello, how may I help you. ")
    while True:
        query = TakeCommand()

        if "exit" in query:
            Speak("OK, you can call me anytime.")
            break

        elif "play" and "on youtube" in query:
            query = query.replace("play","")
            query = query.replace("on youtube","")
            Speak("ok just a second")
            py.playonyt(query)
            
        elif "google search" in query:
            Speak("Ok, This is what I have found on Google")
            query = query.replace("google search","")
            py.search(query)

        elif "time" in query:
            strTime = datetime.datetime.now().strftime("%H:%M:%S") 
            Speak(f"The time is {strTime}")

        elif "date" in query:
            date()

        elif "wikipedia" in query:
            Speak("Searching Wikipedia...")
            query = query.replace("wikipedia", "")
            results = wikipedia.summary(query, sentences=2)
            Speak("According to Wikipedia")
            Speak(results)
            
        elif "open" and "website" in query:
            query = query.replace("open ","")
            query = query.replace(" website","")
            Speak(f"Opening {query} website")
            webbrowser.open(f"www.{query}.com")

        elif "shutdown computer" in query:
            os.system("shutdown /s /t 0")

        elif "restart computer" in query:
            os.system("shutdown /r /t 0")    
        
        elif "alarm" in query:
            Speak("Please tell me the time to set alarm, for example set alarm at 6:30 am")
            tt = TakeCommand()
            tt = tt.replace("set alarm at ","")
            tt = tt.replace(".","")
            tt = tt.upper()
            import MyAlarm
            MyAlarm.alarm(tt)

        elif "start translator" in query:
            translate()
        
        elif "outside" in query:
            temperature()

        elif "internet speed" in query:
            SpeedTest()    
        
        elif "send a whatsapp message" in query:
            Speak("OK, tell me the name or phone number of the person")
            number = TakeCommand()
            Speak("Now tell me the message")
            message = TakeCommand()
            import whatsapp
            whatsapp.whatsapp(number,message)

        elif "how to" in query:
            Speak("OK, searching on internet")
            max_result = 1
            question = search_wikihow(query,max_result)
            assert len(question) == 1
            Speak(question[0].summary)
        
        elif "screenshot" in query:
            pyautogui.hotkey("win","printscreen")
            Speak("Screenshot saved")

        elif "note" in query:
            note()
        
        elif "close file" in query:
            close_notepad()

        elif "battery percentage" in query:
            battery = psutil.sensors_battery()
            Speak(f"{battery.percent}%")
            
        elif "open command prompt" in query:
            os.system("start cmd")
        
        elif "close cmd" in query:
            os.system("TASKKILL /F /im cmd.exe")
            Speak("Command Prompt closed")

        elif "download this video" in query:
            Speak("Video is downloading, you will be notified when the download is completed")
            time.sleep(2)
            pyautogui.click(x=466, y=47)
            pyautogui.hotkey("ctrl","c")
            Link = pyperclip.paste()
            YouTube_Download(Link)
            Speak("Video downloaded. Playing the video")
            Title = YouTube(Link)
            Title = Title.title
            os.startfile(f"E:\\Programming\\AI ASSISTANT\\Database\\Youtube\\{Title}.mp4")

        elif "calculate" in query:
            query = query.replace("calculate","")
            Calculator(query)    

        elif "temperature" in query:
            temp_any(query)  

        elif "volume up" in query:
            pyautogui.press("volumeup")  

        elif "volume down" in query:
            pyautogui.press("volumedown")

        elif "mute" in query:
            pyautogui.press("volumemute")

        elif "whatsapp" in query:
            webbrowser.open("https://web.whatsapp.com/")
        
        elif "take a picture" in query:
            Speak("Taking picture")
            import cam
            cam.take_photo()
            Speak("Picture saved")
                        