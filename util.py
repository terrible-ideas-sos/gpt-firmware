import os
import sys,time,random
from termcolor import colored
import threading

def type_slowly(str):
    time.sleep(.5)
    for letter in str:
        sys.stdout.write(colored(letter, 'green'))
        sys.stdout.flush()
        time.sleep(.05)
    sys.stdout.write("\n")

def system_speak(text):
    try:
        os.system('say ' + text)
    except:
        pass


def say(text):
    speakthread = threading.Thread(target=system_speak, args=(text,))
    speakthread.start()
    type_slowly(" " + text)
