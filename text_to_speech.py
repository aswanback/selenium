#https://gtts.readthedocs.io/en/latest/module.html#languages-gtts-lang
'''
import pyttsx3
engine = pyttsx3.init()
engine.say("I will speak this text")
engine.runAndWait()
'''

import pyttsx3
engine = pyttsx3.init() # object creation
'''
""" RATE"""
rate = engine.getProperty('rate')   # getting details of current speaking rate
print (rate)                        #printing current voice rate
engine.setProperty('rate', 125)     # setting up new voice rate


"""VOLUME"""
volume = engine.getProperty('volume')   #getting to know current volume level (min=0 and max=1)
print (volume)                          #printing current volume level
engine.setProperty('volume',1.0)    # setting up volume level  between 0 and 1

"""VOICE"""
voices = engine.getProperty('voices')       #getting details of current voice
#engine.setProperty('voice', voices[0].id)  #changing index, changes voices. o for male
#engine.setProperty('voice', voices[1].id)   #changing index, changes voices. 1 for female

engine.say("Hello World!")
engine.say('My current speaking rate is ' + str(rate))
engine.runAndWait()
engine.stop()

"""Saving Voice to a file"""
# On linux make sure that 'espeak' and 'ffmpeg' are installed
engine.save_to_file('Hello World', 'test.mp3')
engine.runAndWait()

'''
engine = pyttsx3.init()
import pyttsx3
engine = pyttsx3.init()
v = list(engine.getProperty('voices'))
eng_v = [v[0],v[7],v[10],v[11],v[17],v[28], v[32],v[33],v[37],v[40],v[41]]
print(len(eng_v))
for voice in eng_v:
    engine.setProperty('voice', voice.id)
    engine.say("The houthi creature only desires sleep food and sex: in that order")
engine.runAndWait()


'''
# Import the required module for text  
# to speech conversion 
from gtts import gTTS

# This module is imported so that we can  
# play the converted audio 
import os

# The text that you want to convert to audio 
mytext = "scrump chess, when it crunches, that's why i love, Nestle Crunch "

# Language in which you want to convert 
language = 'en'

# Passing the text and language to the engine,  
# here we have marked slow=False. Which tells  
# the module that the converted audio should  
# have a high speed 
myobj = gTTS(text=mytext, lang=language, slow=False, tld="co.in")

# Saving the converted audio in a mp3 file named 
# welcome  
myobj.save("welcome.mp3")

# Playing the converted file 
os.system("mpg321 welcome.mp3") 
'''