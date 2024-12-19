import pyautogui
from pynput.keyboard import Key, Controller
from time import sleep
from word2number import w2n
import win32gui
import win32con
import requests
from bs4 import BeautifulSoup
import pywhatkit as kit


import ctypes
from time import sleep

from engine.Weilder.services.APPS import open_app,close_app


def temparature():
    url = f"https://www.google.com/search?q={"temparature"}"
    r = requests.get(url)
    data = BeautifulSoup(r.text,"html.parser")
    temp = data.find("div",class_ = "BNeawe").text
    return(f"current temparature is {temp}")

def search(a):
    kit.search(a)   

def volum(a, b):
    questions = a.lower()
    n = b

    # Virtual key codes for volume up and down
    VK_VOLUME_UP = 0xAF
    VK_VOLUME_DOWN = 0xAE

    # Function to simulate key press and release
    def press_key(key_code):
        ctypes.windll.user32.keybd_event(key_code, 0, 0, 0)  # Press key
        ctypes.windll.user32.keybd_event(key_code, 0, 2, 0)  # Release key

    if "up" in questions:
        print("Increasing volume")
        for _ in range(n):
            press_key(VK_VOLUME_UP)
            sleep(0.1)  # Short delay between key presses

    elif "down" in questions:
        print("Decreasing volume")
        for _ in range(n):
            press_key(VK_VOLUME_DOWN)
            sleep(0.1)  # Short delay between key presses

    return a

def protocall(questions):
    if "change window" in questions.lower() :
        pyautogui.hotkey("alt","tab")
        pyautogui.hotkey("alt","tab")
        
    if "terminate" in questions.lower():
        pyautogui.hotkey("alt","f4")
    
    if ("run" or "open") in questions:
        open_app(questions)

    if("quit" in questions):
        if("now" in questions):
            pyautogui.hotkey("alt","tab")
            pyautogui.hotkey("alt","f4")
        else:
            close_app(questions)  

    if questions.lower() == "last stand protocall":
        excluded_title = "Visual Studio Code"

        def callback(hwnd, extra):
            window_text = win32gui.GetWindowText(hwnd).strip()

            # Check if window should be excluded or if it's empty
            if excluded_title.lower() not in window_text.lower() and window_text:
                print(f"Closing window: '{window_text}'")

                if win32gui.IsWindow(hwnd) and win32gui.IsWindowVisible(hwnd):
                    try:
                        # Restore window if minimized before closing
                        win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
                        # Send a close message to the window
                        win32gui.PostMessage(hwnd, win32con.WM_CLOSE, 0, 0)
                    except win32gui.error as e:
                        print(f"Error closing window '{window_text}': {e}")
                else:
                    print(f"Invalid or hidden window handle: '{window_text}'")
            else:
                print(f"Keeping window open: '{window_text}'")

        # Enumerate all windows and apply the callback
        win32gui.EnumWindows(callback, None)

