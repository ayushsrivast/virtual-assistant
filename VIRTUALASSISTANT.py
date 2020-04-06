import webbrowser
import datetime
import warnings
import calendar
import random
import wikipedia
import time
from tkinter import *
from tkinter import ttk
from gtts import gTTS
import playsound
from time import ctime
import speech_recognition as sr
import atexit
import os
import shutil
from twilio.rest import TwilioRestClient


##if os.path.isdir('mp3/audio'):
##    shutil.rmtree('mp3/audio')
##os.mkdir('mp3/audio')

#Ignore any warning messages
warnings.filterwarnings('ignore')

CONTACTS = {"ayush": "917408219005" , "satish":"917408219005"}

def speak(reply):

    print(reply)
    txt2spch=gTTS(text=reply, lang='en')
    txt2spch.save("aud.mp3")

    playsound.playsound("aud.mp3",True)
    os.remove("aud.mp3")


def record():
    voice_in=sr.Recognizer()    
    with sr.Microphone() as source:
        print("Say Something!")
        audio=voice_in.listen(source, timeout=None)	
    command_in=" "
    try:
        command_in=voice_in.recognize_google(audio)
        print("You said: "+command_in)
    except sr.UnknownValueError:
        print("Sorry!! Your Command cannot be recognised!")
    except sr.RequestError:
        print("Sorry!! Couldn't request result from google services!!")
    else:
        pass

    return command_in

def getDate():

    now = datetime.datetime.now()

    my_date = datetime.datetime.today()

    weekday = calendar.day_name[my_date.weekday()] #example friday
    monthNum = now.month
    dayNum = now.day

    #a list of months
    month_names=['January', 'February', 'March', 'April', 'May', 'June', 'July','August', 'September', 'October', 'November', 'December']
    #List of ordinal numbers
    ordinalNumbers= ['1st', '2nd', '3rd', '4th', '5th', '6th', '7th', '8th', '9th', '10th','11th','12th','13th','14th',
    '15th','16th','17th', '18th', '19th', '20th', '21st', '22nd', '23rd', '24th', '25th','26th','27th','28th','29th','30th','31st']

    return 'today is '+weekday+' '+month_names[monthNum-1]+' the '+ordinalNumbers[dayNum-1]+'.'

# A function to return a random greeting response
def greeting(text):

    #greeting inputs
    Greeting_Inputs=['hi', 'hey', 'hola', 'hello','computer']

    #greeting responses
    GREETING_RESPONSES=['howdy', 'whats up', 'hello', 'hey there']

    # if the user input is greeting then return a randomly choosen greeting response
    if text.split()[0].lower() in Greeting_Inputs:
            return random.choice(GREETING_RESPONSES) + '.'
    return ''

# A function to get a person first and last name from text
def getPerson(text):
    wordList = text.split()  # Split the text into a list of words
    for i in range(0, len(wordList)):
        if i + 3 <= len(wordList) - 1 and wordList[i].lower() == 'who' and wordList[i + 1].lower() == 'is':
            return wordList[i + 2] + ' ' + wordList[i + 3]

def getNum(text):
    wordList = text.split()  # Split the text into a list of words
    for i in range(0, len(wordList)):
        if wordList[i].lower() == 'call':
            con = wordList[i + 1]
            if CONTACTS.get(con.lower()) != None:
                print("FOUND CON")
                return CONTACTS.get(con.lower())
        else:
            return False

##            number = int(wordList[i + 2])
##            if number>1000000000 and number < 9999999999:
##                return number
##            else:
##                return 0



TWILIO_PHONE_NUMBER = "+12058395347"
TWIML_INSTRUCTIONS_URL = "http://static.fullstackpython.com/phone-calls-python.xml"

client = TwilioRestClient("AC7a4b1c11fe783347475734403b7d53a3", "a9f941fe101f07d2c802912adae1b0e4")

def dial_numbers(number):
    print("Dialing " + number)
    client.calls.create(to=number, from_=TWILIO_PHONE_NUMBER,
                        url=TWIML_INSTRUCTIONS_URL, method="GET")

	
def virtual_assist(command_in):
    dial = False
    number = 0
    response = ''
    msg="Speak again please"
    flg = 0
    if "what time is it" in command_in:
        msg="The time is: "+ctime()

    if "how are you" in command_in:
        msg="I am fine!"

    if "who are you" in command_in:
        msg = "I am Jarvis. I am a virtual assistant."

    if "search video" in command_in:
        text = command_in.split()
        vid = ""
        for i in range(2, len(text)):
            vid = vid + text[i] + " "
        msg = "searching youtube for video named " + vid
        url = "https://www.youtube.com/results?search_query=" + vid
        webbrowser.open(url)

    if "search web" in command_in:
        text = command_in.split()
        qry=""
        for i in range(2, len(text)):
            qry = qry + text[i] + " "
        msg = "searching on google " + qry
        url = "http://www.google.com/#newwindow=1&q=" + qry
        webbrowser.open(url)

    if "open" in command_in:
        command_in=command_in.split()
        webpage=command_in[1]
        msg="loading "+webpage
        url="http://"+webpage
        webbrowser.open(url)

    if "where is" in command_in:
        command_in=command_in.split()
        location=""
        for i in range(2, len(command_in)):
            location+=command_in[i]
        msg="Locating "+location+" on google maps"
        url="https://www.google.nl/maps/place/"+location

    if "date" in command_in:
        response = ''
        get_Date= getDate()
        response = get_Date

    if "time" in command_in:
        now = datetime.datetime.now()
        hour = ''
        minute = ''
        meridiem = ''
        if now.hour >= 12:
            meridiem = 'p.m' #Post Meridiem (PM), after midday
            hour = now.hour - 12
        else:
            meridiem = 'a.m'#Ante Meridiem (AM), before midday
            hour = now.hour
            
        # Convert minute into a proper string  
        if now.minute < 10:
            minute = '0' + str(now.minute)
        else:
            minute = str(now.minute)

        response = response + ' ' + 'It is ' + str(hour) + ':' + minute + ' ' + meridiem + ' .'
        msg = response

    if('who is ' in command_in):
        person = getPerson(command_in)
        wiki= wikipedia.summary(person, sentences= 2)
        response = response + ' ' + wiki
        msg = response

    if('call ' in command_in):
        number = getNum(command_in)
        if (number!=False):
            msg = 'Calling '+command_in.split()[1]
            dial = True
        else:
            msg = 'Wrong Number'
            
    speak(msg)
    if (dial):
        dial = False
        dial_numbers(number)
        number = 0
        
        

class VA:
    def __init__(self, master):
        self.label=Label(root,text="Command")
        self.label.grid(row=0,column=0)
        self.entry=Entry(root, width=50)
        self.entry.grid(row=0, column=1)
        self.micButton=Button(master,image=photo,command=self.virtual_assist_start)
        self.micButton.grid(row=0,column=4)
        self.searchButton= Button(master, text='Search', width=10, command=self.search)
        self.searchButton.grid(row=0, column=3)
    def virtual_assist_start(self):
        speak("Hi, How can i help you?")
        while 1:
            voice_in=record()
            virtual_assist(voice_in)
    def search(self):
        webbrowser.open('http://google.com/search?q='+self.entry.get())

root=Tk()
root.title("Virtual Assistant")
root.iconbitmap('mic.ico')
photo=PhotoImage(file='mic.png').subsample(30,30)
VA(root)
root.mainloop()
