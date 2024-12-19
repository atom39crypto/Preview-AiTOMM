import multiprocessing
import speech_recognition as sr
import time
import pyautogui as autogui
from facerecog.multi_faces import main
from loadingscreen import display_loading_screen

def startJarvis():
        # Code for process 1
        print("Process 1 is running.")
        from main import start
        start()

def hotword_and_command_listener(r, hotword):

    with sr.Microphone() as source:
        print("Listening for hotword...")
        r.pause_threshold = 1
        r.adjust_for_ambient_noise(source)

        while True:
            try:

                audio = r.listen(source, timeout=10, phrase_time_limit=5) 
                query = r.recognize_google(audio, language='en-in').lower()
                print(f"User said: {query}")

                if hotword in query:
                    print(f"Hotword '{hotword}' detected!")                    
                    
                    autogui.keyDown("win")
                    autogui.press("j")
                    time.sleep(2)
                    autogui.keyUp("win")
                    
                    continue 

            except sr.UnknownValueError:
                print("Didn't understand the audio, waiting for hotword again...")
            except sr.RequestError:
                print("Google Speech Recognition service is unavailable")
            except Exception as e:
                print(f"Error: {e}")

if __name__ == "__main__":
    r = sr.Recognizer()
    hotword = "atom"
    
    image_path = "loading.png"  # Replace with the actual path to your image

    # Start the loading screen in the main thread
    display_loading_screen(image_path)

        # Clear the contents of 'subjects.txt'
    with open('facerecog/sdbjects.txt', 'w') as file:
        file.write('')

    try:
        p3 = multiprocessing.Process(target=main)
        p1 = multiprocessing.Process(target=startJarvis)
        p2 = multiprocessing.Process(target=hotword_and_command_listener, args=(r, hotword))
        p1.start()
        p2.start()
        p3.start()

        p1.join()

        # Terminate p2 and p3 if they are still alive after p1 finishes
        if p2.is_alive():
            p2.terminate()
            p2.join()

        if p3.is_alive():
            p3.terminate()
            p3.join()

        print("System stopped")

    except Exception as e:
        print(f"Error in multiprocessing: {e}")