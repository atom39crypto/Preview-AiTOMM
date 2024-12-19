import os
import pyautogui
import webbrowser
import re
import pygetwindow as gw
import win32gui
from time import sleep
import engine.Weilder.services.contacts as c
from word2number import w2n
from pywhatkit import search
import win32gui
from pywinauto import application
from pywinauto import findwindows
import pygetwindow as gw
import win32gui
import os
import pywintypes
import ctypes
import pyautogui
import time

def catch_site(questions):
    websites = c.website
    website = websites.keys()
    for word in questions.split():
        if word in website:
            return word

def catch_app(questions):
    app = c.apps
    apps = app.keys()
    for word in questions.split():
        if word in apps:
            return word

def find_domains(text):
    # Regular expression pattern for matching domain names
    domain_pattern = r'\b(?:[a-zA-Z0-9-]+\.)+[a-zA-Z]{2,}\b'
    
    # Find all matches in the text
    domains = re.findall(domain_pattern, text)
    
    return domains

def switch_to_chrome():
    try:
        # Find Chrome windows by their title
        chrome_windows = findwindows.find_windows(title_re=".*Chrome.*")
        
        if chrome_windows:
            # Connect to the first Chrome window found
            app = application.Application().connect(handle=chrome_windows[0])
            window = app.window(handle=chrome_windows[0])

            # Bring the Chrome window to the front
            window.set_focus()
            print(f"Switched to: {window.window_text()}")
        else:
            os.system(f"start chrome.exe")
    
    except Exception as e:
        print(f"An error occurred: {e}")

# Call the function

# Call the function
#switch_to_chrome()
def allow_foreground_change():

    hwnd = win32gui.GetForegroundWindow()  # Get current foreground window
    ctypes.windll.user32.AllowSetForegroundWindow(ctypes.windll.user32.GetWindowThreadProcessId(hwnd, 0))

def open_app(a):
    print(f"<----------------------------------{a}------------------------------>")
    questions = a
    try:
            if("chromeApps" in questions):
                switch_to_chrome()
                return a
            apps = c.apps
            keys = apps.keys() 
            for app in apps.keys():
                if app.lower() in questions.lower():
                    print(f"Looking for windows with the title containing: {app}")
                    # Find all windows with titles containing the app name (case insensitive)
                    windows = gw.getWindowsWithTitle(app.capitalize())

                    if windows:
                        for window in windows:
                            hwnd = window._hWnd  # Get the window handle (HWND)

                            # Try to allow foreground change
                            try:
                                allow_foreground_change()
                                win32gui.ShowWindow(hwnd, 9)  # Restore the window if minimized
                                time.sleep(0.5)  # Small delay to ensure the window is restored
                                win32gui.SetForegroundWindow(hwnd)  # Bring to foreground
                                print(f"Restored and switched to: '{window.title}' (HWND: {hwnd})")
                            except pywintypes.error as e:
                                print(f"Error bringing window to foreground: {e}")
                                print("Simulating Alt+Tab to switch to the window.")
                                pyautogui.hotkey('alt', 'tab')  # Simulate Alt+Tab
                                time.sleep(0.5)
                                win32gui.SetForegroundWindow(hwnd)
                            return  a# Exit after handling the first match
                    else:
                        # If no window is found, start the application
                        print(f"No running window found for {app}. Starting {app} minimized.")
                        os.system(f"start {apps[app]}.exe")
                        return a
    except:

        pyautogui.press("super")
        pyautogui.typewrite(questions)
        pyautogui.press("enter")
        return a
    


def webpage(a):
    if len(a)>0:

        webbrowser.open(f"{a}")
    else:
        search(a)
    return a


def closetab(a):
        switch_to_chrome()
        i = 0
        while(i<a):
            pyautogui.hotkey("ctrl","w")
            sleep(1)
            i=i+1
        return str(a)
        
def close_app(a):

    apps = c.apps
    print(apps)
    keys = apps.keys()
    print(keys)
    print("Quitting .......... ")
    for app in keys:
        if app in a:
            os.system(f"taskkill /f /im {apps[app]}.exe")

    return a