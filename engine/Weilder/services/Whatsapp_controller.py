import pywhatkit as kit
import engine.Weilder.services.contacts as c
import time
# Get the current time
import time

contact = c.contact
contacts = contact.keys()

def whats_app(a,b):
    print("text initializing.......")
    reciver = a
    print(reciver)
    if (reciver in contact):
        current_time = time.localtime()
        current_hour = current_time.tm_hour
        current_minute = current_time.tm_min + 1  # Add one minute
        if current_minute == 60:
            current_minute = 0
            current_hour += 1

        try:
            reciver = (contact.get(reciver))
            kit.sendwhatmsg(reciver,b, current_hour, current_minute)
            print("Message scheduled successfully.")
        except Exception as e:
            print(f"An error occurred: {e}")

    else:
        print("well shit")  

    return b  

#whats_app("Text didi whatsup ?")