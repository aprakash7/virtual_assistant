# -*- coding: utf-8 -*-
"""
Created on 19/07/2021
@author: Akshay Prakash
"""


import pyaudio
import speech_recognition as sr
import pyttsx3
import time
import pywhatkit
import datetime
import wikipedia
import pyjokes
import webbrowser
import os
import subprocess
from ecapture import ecapture as ec
import wolframalpha
import json
import requests

#listen
listener = sr.Recognizer()

#initalise engine
engine= pyttsx3.init()
engine.setProperty('rate', 170)
voices= engine.getProperty('voices')

for voice in voices:
    id= "ID: %s" %voice.id
    #print("ID: %s" %voice.id)

#Insert your HKEY for the narrator's voices
#Eg: voice_id = "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\MSTTS_V110_enGB_GeorgeM"
voice_id = "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\MSTTS_V110_enGB_GeorgeM"
engine.setProperty('voice', voice_id)

#start engine
def talk(text):
    engine.say(text)
    engine.runAndWait()

#Greet
def wishMe():
    hour=datetime.datetime.now().hour
    if hour>=0 and hour<12:
        speak("Hello,Good Morning")
        print("Hello,Good Morning")
    elif hour>=12 and hour<18:
        speak("Hello,Good Afternoon")
        print("Hello,Good Afternoon")
    else:
        speak("Hello,Good Evening")
        print("Hello,Good Evening")
        
#Take command
def take_command():
    try:
        #Pass if not recognized
        #use micophone as source and call the speech recognzier to listen to the source
        with sr.Microphone() as source:
            print('listening..')
            voice= listener.listen(source)
            command= listener.recognize_google(voice)
            command= command.lower() #necessary for print
    except:
        pass
    return command

#Function for while 
def run_bot():
    command= take_command()
    #print(command)

    #exit
    if 'bye' in command or 'stop' in command or 'see you' in command or 'thank you' in command:
        talk('I will see you again friend')
        print('Shutting down')
        exit()
    
    #Songs
    elif 'play' in command:
        #Songs on Youtube
        song= command.replace('play', '')
        talk('Playing'+ song)
        pywhatkit.playonyt(song)
    
    #Time
    elif 'time' in command:
        #Return hours and minutes, 1 to 12 hr %I
        current_time= datetime.datetime.now().strftime('%I %M %p')
        talk('It is'+ current_time + 'in India now')
        print(current_time)
    
    #Gain information
    elif 'wikipedia search' in command:
        #wikipedia information (object, no of lines)
        try:
            object= command.replace('wikipedia search', '')
            info = wikipedia.summary(object, sentences=1, auto_suggest= True)
            print(info)
            talk(info)
            time.sleep(2)
            talk('Do you want me to give you a brief information?')
            command= take_command()

            if 'yes' in command:
                talk('Okay')
                #command= command.replace('yes', '')
                extra_results= wikipedia.summary(object, sentences= 5)
                talk(extra_results)
            else:
                talk('Okay, let me know if you need anything else')

        except wikipedia.exceptions.DisambiguationError as e:
            talk('I cannot figure what you are asking particularly. Here is a list for you.')
            time.sleep(1)
            talk(e.options)
            talk('These are the options available. What do you want me to search')
        #pluton

        except wikipedia.exceptions.PageError as page_error:
            talk('Your search does not match any pages. Please try again')

    #tell a joke
    elif 'joke' in command:
        talk(pyjokes.get_joke())

    #open gmail
    elif 'open gmail' in command:
        talk('Okay')
        webbrowser.open_new_tab('gmail.com')
        talk('Your Gmail is open now')

    #just open Google
    elif 'open google' in command:
        talk('Opening google in new tab')
        webbrowser.open_new_tab('www.google.com')
        talk('Let me know if you need anything else')

    #just open YouTube
    elif 'open youtube' in command:
        talk('Opening YouTube')
        webbrowser.open_new_tab('www.youtube.com')
        talk('Youtube is open now')

    #search on google
    elif 'search' in command:
        the_keyword= command.replace('search', '')
        pywhatkit.search(the_keyword)
        talk('Searching' + the_keyword)

    #latest news
    elif 'pluton news' in command:
        talk('Displaying latest news for you')
        news= webbrowser.open_new_tab('https://timesofindia.indiatimes.com/home/headlines')

    elif 'latest science news' in command:
        talk('Displaying latest scientific discoveries and inventions for you')
        news= webbrowser.open_new_tab('https://www.sciencedaily.com/news/top/science/')
        news_2= webbrowser.open_new_tab('https://www.livescience.com/news')

    #ecapture
    #accepts 3 parameters, first connected index is 0
    elif 'take a photo' in command or 'capture' in command:
        talk('Say cheeeeeeeeeeeeeeeeese')
        ec.capture(0, 'robo camera', 'img.jpg')

    #search on the internet
    elif 'open website' in command:
        command= command.replace('open website', '')
        webbrowser.open_new_tab(command)
        talk('Opened' + command)

         #Create wolfram alpha account and insert your UNIQUE-> app_id
         #listens two times in this statement
    elif 'question' in command:
        talk('I can answer to computational and geographical questions, what question do you want to ask now?')
        question=take_command() # give question
        app_id=" "
        client = wolframalpha.Client(app_id) #instance of class wolframalpha
        res = client.query(question) #res stores the response
        answer = next(res.results).text
        talk(answer)
        print(answer)

    #elif 'start' in command:
    #    talk('tell me what to run')
    #    app_name= take_command()
    #    os.system(str(app_name))

    #subprocess can execute other programs
    #shut down /l means log off
    elif 'terminate' in command:
        talk('Okay')
        talk('Your PC will shut down in 60 seconds, please make sure you have saved and closed all applications')
        subprocess.call(['shutdown', '/s'])

    else:
        talk('My bad')
        talk('Could you repeat?')

while True:
    wishMe()
    run_bot()
