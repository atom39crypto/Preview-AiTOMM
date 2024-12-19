import tkinter as tk
from PIL import Image, ImageTk
import time
import multiprocessing
import speech_recognition as sr
import threading

# Function to display the loading screen
def display_loading_screen(image_path):
    # Initialize the Tkinter root window
    root = tk.Tk()
    root.title("Loading...")

    # Remove the window's border for a clean look
    root.overrideredirect(True)

    # Load the image using PIL
    image = Image.open(image_path)

    # Resize the image to half its original size
    width, height = image.size
    image = image.resize((width // 2, height // 2))

    # Convert the image to a format Tkinter can use
    photo = ImageTk.PhotoImage(image)

    # Create a Label widget to display the image
    label = tk.Label(root, image=photo)
    label.pack()

    # Center the window on the screen
    window_width = image.width
    window_height = image.height
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    position_top = (screen_height // 2) - (window_height // 2)
    position_right = (screen_width // 2) - (window_width // 2)
    root.geometry(f"{window_width}x{window_height}+{position_right}+{position_top}")

    # Display the window and update it
    root.update()

    # Allow loading screen to remain for 5 seconds, then close
    time.sleep(5)

    # Close the loading screen
    root.destroy()
