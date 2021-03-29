import pyttsx3
import speech_recognition as sr
import datetime
import os
import random
from requests import get
import wikipedia
import webbrowser
import requests
import smtplib
import sys
import pyjokes
import pyautogui
import time
import PyPDF2
import pytube
from bs4 import BeautifulSoup

engine = pyttsx3.init()
voices = engine.getProperty("voices")
engine.setProperty("voices", voices[1].id)


class social_media():
    def open_facebook(self):
        webbrowser.open("https://www.facebook.com/")

    def open_instagram(self):
        webbrowser.open("https://www.instagram.com/")

    def open_linkedin(self):
        webbrowser.open(
            "https://www.linkedin.com/feed/?trk=guest_homepage-basic_nav-header-signin")

    def open_github(self):
        webbrowser.open("https://github.com/")


class system_apps():
    def speak(self, audio):
        engine.say(audio)
        engine.runAndWait()

    def open_notepad(self):
        path = "C:\\ProgramData\\Microsoft\\Windows\\Start Menu\\Programs\\Accessories\\Notepad"
        os.startfile(path)

    def open_google(self):
        path = "C:\\ProgramData\Microsoft\\Windows\\Start Menu\\Programs\\Google Chrome"
        self.speak("what do you want to search on google sir")
        search = self.take_command().lower()
        self.speak("opening google")
        webbrowser.open(search)

    def open_command_prompt(self):
        self.speak("opening command prompt")
        os.system("start cmd")


class jarvis_abilites():
    def speak(self, audio):
        engine.say(audio)
        engine.runAndWait()

    def taking_screen_shot(self):
        print("sir,please tell me the name of this screenshot file")
        self.speak("sir,please tell me the name of this screenshot file")
        name = self.take_command().lower()
        print("Hang on for few seconds sir , I am taking the screenshot")
        self.speak("Hang on for few seconds sir , I am taking the screenshot")
        time.sleep(3)
        img = pyautogui.screenshot()
        img.save(f"{name}.jpg")
        print("ok sir i am done with taking screenshot,it is saved in our current folder,i am ready for another command sir")
        self.speak(
            "ok sir i am done with taking screenshot, it is saved in our current folder, i am ready for another command sir")

    def audio_book(self):
        # note: book should be in this dorectory,or you can enter the location of book in open commmand
        book = open("TOM.pdf", 'rb')
        # opening the book in binary mode
        pdfreader = PyPDF2.PdfFileReader(book)
        # intilaising the reader,creating the object of the module
        pages = pdfreader.numPages
        # getting total no of pages
        self.speak(f"This book consists of {pages} pages")
        self.speak("sir,please say which page i should read")
        self.speak("Enter the page number")
        # getting the page no to which we should read
        page_no = int(input("Enter the page no : "))
        print(page_no)
        # getting the page
        page = pdfreader.getPage(page_no)
        # extracting the text from the page
        text = page.extractText()
        print(text)
        self.speak(text)

    def find_location(self, shout=True):
        try:
            r = requests.get("https://get.geojs.io/")
            ip_request = requests.get("https://get.geojs.io/v1/ip.json")
            ip_address = ip_request.json()['ip']

            url = "https://get.geojs.io/v1/ip/geo/" + ip_address + ".json"
            # # url to get the location
            geo_requests = requests.get(url)
            geo_data = geo_requests.json()

            # # it will give data in the form of dictonary
            # # it mnay throw error sometimws because there may be no state for some plcaes like delhi
            city = geo_data['city']
            state = geo_data['region']
            country = geo_data['country']
            if shout:
                print(ip_address)
                print(geo_data)
                print(
                    f"Sir we are in {city} city in {state} region of  {country}")
                speech = f"Sir we are in {city} city in {state} region of  {country}"
                self.speak(speech)
            return city
        except:
            self.speak(
                "Sorry sir,due to poor internet i cannot find the location")
            # finding location takes more time ,so we added exception.
            pass

    def youtube_video_download(self):
        self.speak("sir, please enter the youtube video url")
        link = input("Enter the video url ")
        video = pytube.YouTube(link)
        stream = video.streams.get_highest_resolution()
        self.speak("hang on sir,video is downloading in current folder")
        stream.download()
        self.speak("ok sir,youtube video is downloaded ,you may proceed further")

    def search_wikipedia(self, query):
        print("searching wikipedia.....")
        self.speak("searching wikipedia")
        query = query.replace("wikipedia", "")
        results = wikipedia.summary(query, sentences=3)
        print(results)
        self.speak("according to wikipedia")
        self.speak(results)

    def weather_forecast(self, talk=True):
        place = self.find_location(shout=False)
        weather = "temperature in " + place
        url = f"https://www.google.com/search?q={weather}"
        r = requests.get(url)
        content = BeautifulSoup(r.text, "html.parser")
        temperature = content.find("div", class_="BNeawe").text
        if talk:
            print(f"current {weather} is {temperature}")
            self.speak(f"current {weather} is {temperature[:2]} degrees") 
        else:
            return temperature


class jarvis_code(social_media, system_apps, jarvis_abilites):

    def speak(self, audio):
        engine.say(audio)
        engine.runAndWait()

    def take_command(self):
        r = sr.Recognizer()
        with sr.Microphone() as source:
            print("Listening....")
            audio = r.listen(source, timeout=5, phrase_time_limit=5)
        try:
            print("Recognizing....")
            query = r.recognize_google(audio, language="en-in")
            print(query)
        except sr.RequestError:
            return "poor connection"
        except:
            return None
        return query.lower()

    def wish(self):
        hour = int(datetime.datetime.now().hour)
        minute = int(datetime.datetime.now().minute)
        temp = self.weather_forecast(talk=False)
        if hour >= 0 and hour <= 12:
            self.speak(
                f"Good morning , it's {hour} {minute}  a m , temperature outside is ,{temp[:2]} degrees ") 
            print(
                f"Good morning , it's {hour} : {minute} A.M. Temperature outside is ,{temp}")
        elif hour > 12 and hour <= 18:
            self.speak(
                f"Good Afternoon , it's {hour-12}  {minute} p m , temperature outside is ,{temp[:2]} degrees")
            print(
                f"Good afternoon ,it's {hour-12} : {minute} P.M.Temperature outside is ,{temp} ")
        else:
            self.speak(
                f"Good Evening , it's {hour-12}  {minute} p m , temperature outside is ,{temp[:2]} degrees") 
            print(
                f"Good evening,it's {hour-12} : {minute} P.M. Temperature outside is ,{temp}")
        self.speak("Hii Sir, I am jarvis, please tell how can i help you")

    def desire(self):
        while True:
            # opening the system apps
            # opening notebook
            query = self.take_command()
            if query == None:
                pass
            elif "open notepad" in query:
                self.speak("opening notepad")
                self.open_notepad()

            # openiong the google chrome
            elif "open google" in query:
                self.open_google()

            # opening command prompt
            elif "open command prompt" in query:
                self.speak("opening command prompt")
                self.open_command_prompt()

            # opening the github
            elif "open github" in query:
                self.speak("opening the github")
                self.open_github()

            # playing the music
            elif "play music" in query:
                music_directory = "E:\\Music\\english"
                songs = os.listdir(music_directory)
                random.shuffle(songs)
                for song in songs:
                    if song.endswith(".mp3"):
                        os.startfile("E:\\Music\\english\\"+song)

            # getting ip address
            elif "ip address" in query:
                ip = get("https://api.ipify.org").text
                print(ip)
                self.speak(f"sir your ip address is {ip}")

            # performing the online tasks

            # searching for something in wikipedia
            elif "wikipedia" in query:
                self.search_wikipedia(query)

            # opening youtube
            elif "open youtube" in query:
                self.speak("opening youtube")
                webbrowser.open("www.youtube.com")

            # opening facebook
            elif "open facebook" in query:
                self.speak("opening facebook")
                self.open_facebook()

            # opening instagrasm
            elif "open instagram" in query:
                self.speak("opening instagram")
                self.open_instagram()

            # opening linkedin
            elif "open linkedin" in query:
                self.speak("opening linkedin")
                self.open_linkedin()

            # playing song on youtube
            elif "play songs on youtube" in query:
                self.speak("playing songs on youtube")
                kit.playonyt("never lie to me")

            # making jarvis to go to sleep
            elif "go to sleep" in query:
                self.speak(
                    "Ok sir i am going to sleep,you can call me anytime")
                break

            # terminating the programm execution
            elif "go offline" in query:
                self.speak("Thank you sir for using me,have a nice day")
                sys.exit()

            # shutdowning the sysytem
            elif "shutdown" in query:
                self.speak("Got it Sir, shutdowning the Pc,")
                self.speak("Thank you Sir,Have a nice day")
                os.system("shutdown /s /t 5")

            # restarting the computer
            elif "restart" in query:
                self.speak("Hang on Sir, restarting the Pc")
                os.system("shutdown /r /t 5")

            # saying the jokes
            elif "joke" in query:
                joke = pyjokes.get_joke()
                self.speak(joke)

            # finding the location
            elif "where i am " in query or "location" in query:
                self.find_location()

            # taking the screenshot
            elif "take screenshot" in query or "screenshot" in query:
                self.taking_screen_shot()

            # reading the pdf
            elif "read book" in query:
                self.audio_book()

            # downloading the youtube video
            elif "download youtube" in query or "download" in query:
                self.youtube_video_download()

            elif "temperature" in query:
                self.weather_forecast()


jarvis = jarvis_code()
# jarvis.speak("hello sir how can i help you")
while True:
    query = jarvis.take_command()
    if "poor connection" == query:
        jarvis.speak(
            "Sir,due to poor internet connection , i am not able to follow your commands, please connect to internet sir")
        jarvis.speak(
            "sir,i will wait for 10 seconds, for you to connect to internet ")
        time.sleep(10)
        jarvis.speak("ok sir i am done,i hope your are connected to internet")
        query = jarvis.take_command()
        if "poor connection" == query:
            jarvis.speak(
                "sir, i think you don't have proper intenet connection, so i am going offline")
            sys.exit()
    elif None == query:
        pass
    elif "hello jarvis" in query:
        jarvis.wish()
        # query = jarvis.take_command()
        jarvis.desire()

# this is for testing
