import sqlite3
import eel

from engine.command import speak

con = sqlite3.connect("atom.db")
cursor = con.cursor()
# starting sound
@eel.expose
def playAssistantSound():
    speak("I am Atom ")
    