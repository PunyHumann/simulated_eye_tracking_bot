import speech_recognition as sr
import pyttsx3
import queue
import socket
from ollama import Client
from ollama import chat

#TCP Deffinitions
IP_ADDRESS = "127.0.0.1"
PORT_NUM = 5009
BUFFER_SIZE = 8192
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#client_socket.connect((IP_ADDRESS, PORT_NUM))


#Ollama setup
client = Client()
response = client.create(
    model = 'CUBE',
    from_='llama3.2:3b',
    system="""You are a witty floating cube assistant who speaks in brief sentences""",
    stream=False
)
messages = []

#------------------------------------------------------------------------------------

# SPEAH TO TEXT

# Creating Text queue for stt -> Ollama
text_q = queue.Queue(maxsize=0)

# Stt setup
recognizer = sr.Recognizer()
mic = sr.Microphone()
with mic:
    recognizer.adjust_for_ambient_noise(mic, duration=0.5)

#This fn will be called by background audio thread
def background_callback(recognizer, audio):
    global text_q
    try:
        print("Mic Listening:")
        text = recognizer.recognize_google(audio)
            
        #Resulting text string
        text = text.lower()
        text_q.put(text)
        #print("TEXT: ", text)

    except sr.RequestError as e:
        print(f"ERROR: {e}")
        
    except sr.UnknownValueError:
        print("Didn't understand you...")
        
    except KeyboardInterrupt:
        print("Program terminated by user...")

#innitializing background stt thread
stop_listening = recognizer.listen_in_background(mic, background_callback)

#------------------------------------------------------------------------------------

# OLLAMA CHAT LOOP

# Main loop (press 'q' to quit)
try:
    while True:
        # Ollama Chat with history
        try:
            new_message = text_q.get_nowait()
            print(new_message)
            chat_response = chat(
                'CUBE',
                messages=[*messages, {'role': 'user', 'content': new_message}]
            )

            # merging past messages with current to conserve history
            messages += [
                {'role': 'user', 'content': new_message},
                {'role': 'assistant', 'content': chat_response.message.content}
                ]
            print(chat_response.message.content + '\n')
            #client_socket.send(chat_response.message.content.encode())
        except queue.Empty:
            continue
except (KeyboardInterrupt, SystemExit):
    stop_listening(wait_for_stop=False)
    #client_socket.close()