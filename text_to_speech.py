'''
import pyttsx3
engine = pyttsx3.init() # object creation

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

import pyttsx3
engine = pyttsx3.init()
v = list(engine.getProperty('voices'))
new_v = [v[0],v[7],v[10],v[11],v[17],v[28], v[32],v[33],v[37],v[40],v[41]]
voice_list = []
lang_list = []
for voice in new_v:
    print(f'age: {voice.age}  gender: {voice.gender}  id: {voice.id}  languages: {voice.languages}  name:{voice.name}')
    engine.setProperty('voice', voice.id)
    if 'en' in voice.languages[0]:
        voice_list.append(voice.id)
        lang_list.append(voice.languages[0])
    engine.say("I'm an engineer!")
#print(voice_list)
#print(lang_list)
#engine.runAndWait()

# https://pyttsx3.readthedocs.io/en/latest/engine.html
# English speakers: Alex    daniel  fiona       Fred    karen   moira   rishi   samantha    tessa   veena   Victoria
# Dialect:          en_US   en_GB   en-scotland en_US   en_AU   en_IE   en_IN   en_US       en_ZA   en_IN   en_US


# https://gtts.readthedocs.io/en/latest/module.html#localized-accents
'''
from gtts import gTTS
import os
mytext = 'I have genital herpes'
language = 'en'
myobj = gTTS(text=mytext, lang=language, slow=False,tld='co.uk')
myobj.save("welcome.mp3")
os.system("mpg321 -g 100 welcome.mp3")
'''
