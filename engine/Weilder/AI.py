import keyboard
import threading 
import json
import keyboard  # Library to detect key presses
from groq import Groq
import tiktoken
import datetime
import speech_recognition as sr  # Speech Recognition to detect 'stop'

from engine.Weilder.memory import *
from engine.command import speak
from engine.Weilder.services.youtube_controll import *
from engine.Weilder.services.APPS import *
from engine.Weilder.services.Small_Functions import *
from engine.Weilder.services.write import write
from engine.Weilder.Location import location
from facerecog.multi_faces import save_name
from engine.Weilder.services.Whatsapp_controller import whats_app
from engine.Weilder.services.update import update

# <-------------------------------global variables -------------------------------->

client = Groq()

tokenizer = tiktoken.get_encoding("cl100k_base")

history_file_path = 'engine\Weilder\memory.json'

now = datetime.datetime.now()
date_time = now.strftime("%Y-%m-%d %H:%M:%S")

conversation_history = load_conversation_history()

continue_speaking = True
speaking_done = False

system_tools = [
    #face_save
        {
            "type": "function",
            "function": {
                "name": "User_name",
                "description": "saves user's name that is provided bu the user",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "a": {
                            "type": "string",
                            "description": "user's name provided bu the user"
                        },
                    },
                    "required": ["a"]  # Only require the video name
                },
            },
        },
    # write
        {
            "type": "function",
            "function": {
                "name": "write",
                "description": "Creates a new either coding file or word file",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "a": {
                            "type": "string",
                            "description": "File name with extension"
                        },
                        "b": {
                            "type": "string",
                            "description": "Content of the file provided by the AI/LLM"
                        },
                    },
                    "required": ["a", "b"]  # Updated required fields
                },
            },
        },
    #volume
        {
        "type": "function",
        "function": {
            "name": "volum",
            "description": "Increases or decreases the volume.",
            "parameters": {
            "type": "object",
            "properties": {
                "a": {
                "type": "string",
                "description": "Specify 'up' to increase volume or 'down' to decrease volume."
                },
                "b": {
                "type": "integer",
                "description": "The number of steps to increase or decrease the volume."
                }
            },
            "required": ["a", "b"]
            }
        }
        },
    #updating
        {
            "type": "function",
            "function": {
                "name": "update",
                "description": "Updates a contact with a new phone number or performs an action like insert or delete.",
                "parameters": {
                "type": "object",
                "properties": {
                    "a": {
                    "type": "string",
                    "description": "The name of the contact to update."
                    },
                    "b": {
                    "type": "integer",
                    "description": "The new contact number to be assigned."
                    },
                    "c": {
                    "type": "string",
                    "description": "The action to perform: 'insert' or 'delete' the contact."
                    }
                },
                "required": ["a", "b", "c"]
                }
            }
        },
    #temparature
        {
            "type": "function",
            "function": {
                "name": "search",
                "description": "Searches the specified query in the browser.",
                    "parameters": {
                    "type": "object",
                        "properties": {
                            "a": {
                                "type": "string",
                                "description": "The query or question to be searched in the browser."
                            }
                        },
                        "required": ["a"]
                    }
                }
        },

    #APPS
        {
            "type": "function",
            "function": {
                "name": "open_app",
                "description": "open the app",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "a": {
                            "type": "string",
                            "description": "name of the app to be run/opened"
                        },
                    },
                    "required": ["a"]  # Only require the video name
                },
            },
        },
        {
        "type": "function",
        "function": {
            "name": "close_app",
            "description": "Quits or closes the specified application.",
            "parameters": {
            "type": "object",
            "properties": {
                "a": {
                "type": "string",
                "description": "The name of the application to quit or close."
                }
            },
            "required": ["a"]
            }
        }
        },

    #youtube
        {
            "type": "function",
            "function": {
                "name": "youtube",
                "description": "Plays videos on YouTube",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "a": {
                            "type": "string",
                            "description": "Name of the video"
                        },
                    },
                    "required": ["a"]  # Only require the video name
                },
            },
        },
        {
            "type": "function",
            "function": {
                "name": "video_controller",
                "description": "Controls video actions such as pause/unpause, mute/unmute, and forward/back.",
                "parameters": {
                "type": "object",
                "properties": {
                    "a": {
                    "type": "string",
                    "description": "Action to be performed. Valid values: 'pause', 'unpause', 'mute', 'unmute', 'forward', 'back'."
                    },
                    "b": {
                    "type": "integer",
                    "description": "Amount or vector associated with the action. For 'forward' and 'back', it specifies the number of seconds. default 1"
                    }
                },
                "required": ["a","b"]
                },
            },
        },

    #webpage
        {
            "type": "function",
            "function": {
                "name": "webpage",
                "description": "open website in web browser",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "a": {
                            "type": "string",
                            "description": " link of the web page provided by AI/LLM "
                        },
                    },
                    "required": ["a"]  # Only require the video name
                },
            },
        },
        {
            "type": "function",
            "function": {
                "name": "closetab",
                "description": "Closes tabs in a web browser.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "a": {
                            "type": "integer",
                            "description": "Number of tabs to be closed. Default is 1."
                        },
                    },
                    "required": ["a"]  # Number of tabs to close is required
                },
            },
        },
    
    #Whats_app
        {
            "type": "function",
            "function": {
                "name": "whats_app",
                "description": "sends massage/text in whats app",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "a": {
                            "type": "string",
                            "description": "name of the reciver"
                        },
                        "b": {
                            "type": "string",
                            "description": "massage to be sent"
                        },
                    },
                    "required": ["a", "b"]  # Updated required fields
                },
            },
        },
        


    
    ]

#<--------------------------------Functions of the file ---------------------------->
# Function to speak text




def stop_speaking():
    global continue_speaking
    continue_speaking = False
    print("stop_speaking() called - continue_speaking set to False.")

def listen_for_stop():
    global continue_speaking, speaking_done
    recognizer = sr.Recognizer()
    mic = sr.Microphone()

    with mic as source:
        recognizer.adjust_for_ambient_noise(source)
        print("Listening for 'stop' command...")

        while continue_speaking and not speaking_done:
            try:
                audio = recognizer.listen(source, timeout=5)
                recognized_text = recognizer.recognize_google(audio).lower()
                print(f"Recognized: {recognized_text}")

                if "stop" in recognized_text:
                    stop_speaking()
                    break
            except sr.UnknownValueError:
                continue
            except sr.RequestError as e:
                print(f"Error requesting results: {e}")
                break
            except sr.WaitTimeoutError:
                print("Listening timeout, retrying...")
                continue

    print("Stopping listener thread...")
def core(prompt,person):
    tools = system_tools
    
    with open('facerecog/sdbjects.txt', 'r') as file:
        objects = file.read()  # Reads the entire file content as a string
    
    system_message = {
            "role": "system",
            "content": f"""
                        Your name is AiTOMM cronounced as Atom. Answer in simple sentences;
                        The objects around them are {objects} person infont of you is{person}
                        who is sending the prompt every single time before answering! don't  just say it from previous conversation.
                        you are an Device assistant and you have the ability to
                        play youtube video,forward/rewing video,mute/unmute said video and pause unpause the latter
                        run and quit Apps , twik the device volume,text in whats app,open and close websites/tabs,
                        when asked for these services don't say more than 5 words, 
                        current time is: {time.strftime('%Y-%m-%d %H:%M:%S')},and the Temparature is {temparature()}.
                        and adapt to the culture of {location()} but never the language unless asked for always use English as your language.
                        Special protocalls {protocall(prompt)}.
                        """
        }

    messages = [system_message]  
    messages.extend(conversation_history) 
    messages.append({'role': 'user', 'content': prompt})


    response = client.chat.completions.create(
        messages=messages,
        tools=tools,
        model="llama3-70b-8192",
        tool_choice="auto",
        temperature=1,
        max_tokens=4096,
    )

    # Get the response message
    response_message = response.choices[0].message
    tool_calls = response_message.tool_calls if hasattr(response_message, 'tool_calls') else []

    print("First LLM Call (Tool Use) Response:", response_message)

    # Step 2: Check if the model wanted to call a function
    if tool_calls:
        # Step 3: Call the function and append the tool call to our list of messages
        available_functions = {
            "write": write,
            "volum":volum,
            "update":update,
            "search":search,

            "open_app":open_app,
            "close_app":close_app,

            "youtube": youtube,            
            "video_controller":video_controller,

            "webpage":webpage,
            "closetab":closetab,

            "whats_app":whats_app,

            "User_name": save_name
        }

        # Process each tool call
        for tool_call in tool_calls:
            function_name = tool_call.function.name
            function_to_call = available_functions[function_name]
            function_args = json.loads(tool_call.function.arguments)

            # Handle the youtube function separately since it only requires one argument
            if function_name in ("youtube", "webpage","closetab","User_name","open_app","close_app","search"):
                function_response = function_to_call(
                    a=function_args.get ("a"),
                )
            elif function_name in ("update"):
                function_response = function_to_call(
                    a=function_args.get("a"),
                    b=function_args.get("b"),
                    c=function_args.get("c"),
                    
                )
            else:
                function_response = function_to_call(
                    a=function_args.get("a"),
                    b=function_args.get("b"),
                )

            # Append the function response to messages
            messages.append(
                {
                    "tool_call_id": tool_call.id,
                    "role": "tool",
                    "name": function_name,
                    "content": function_response,
                }
            )  # Extend conversation with function response

        # Send the result back to the LLM to complete the chat
        second_response = client.chat.completions.create(
            model="llama3-70b-8192",  # Use the same model as before
            messages=messages
        )  # Get a new response from the model where it can see the function response

        print("\n\nSecond LLM Call Response:", second_response.choices[0].message.content)
        return second_response.choices[0].message.content  # Return the final response

    return response_message.content  # Return the initial response if no tool calls were made

def mainframe(text):
    
    file = open('facerecog/currentface.txt', 'r')
    person = file.read()
    file.close()

    person_list = person.split() 

    person = list(set(person_list))

    print(person) 

    print(f"<----------------------------{person}----------------------->")

    content = f"{text} (sent on: {date_time} by {person})" 
    update_conversation_history(conversation_history,"user",content)

    text = core(text,person)
    update_conversation_history(conversation_history,"assistant",text)

    # Add hotkey listener for 'esc'
    keyboard.add_hotkey('esc', stop_speaking)
    print("Press 'esc' or say 'stop' to interrupt.")

    global continue_speaking, speaking_done
    continue_speaking = True
    speaking_done = False  # Reset flag for each session

    # Add hotkey listener for 'esc'
    keyboard.add_hotkey('esc', stop_speaking)
    print("Press 'esc' or say 'stop' to interrupt.")

    # Start listening for "stop"
    stop_listening_thread = threading.Thread(target=listen_for_stop)
    stop_listening_thread.start()

    words = text.split()
    for i in range(0, len(words), 10):
        if not continue_speaking:  # Check the flag
            print("Speaking stopped by user.")
            break

        chunk = words[i:i+10]
        parts = " ".join(chunk)
        print(f"Speaking: {parts}")
        speak(parts)
        time.sleep(1)  # Simulate delay for speaking

    # Mark speaking as done
    speaking_done = True
    print("Speaking complete.")

    # Ensure the listener thread terminates if running
    stop_listening_thread.join()  
    print("Exiting program cleanly.")




#<--------------------------------------- Test ------------------------------------->

if __name__ == "__main__":
    response = mainframe("write a word file for volcano")

    