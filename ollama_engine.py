import speech_recognition as sr
import pyttsx3
import queue
import keyboard
from ollama import Client
from ollama import chat

#Ollama setup: https://github.com/ollama/ollama-python/tree/main/examples
#Ollama Client settup
client = Client()
response = client.create(
    model = 'CUBE',
    from_='llama3.2:3b',
    system='You are a sarcastic supergenious cube who' \
    'works as a primary advisor to whoever asks you anything.',
    stream=False
)
messages = []

#Creating Text queue for stt -> Ollama
text_q = queue.Queue(maxsize=0)

#stt reference: https://www.geeksforgeeks.org/python/python-convert-speech-to-text-and-text-to-speech/
#stt background reference: https://github.com/Uberi/speech_recognition/blob/master/examples/background_listening.py
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

# Main loop (press 'q' to quit)
# Ollama Chatting with History refference https://github.com/ollama/ollama-python/blob/main/examples/chat-with-history.py
while not keyboard.is_pressed('q'):
    try:
        new_message = text_q.get_nowait()
        print(new_message)
        chat_response = chat(
            'CUBE',
            messages=[*messages, {'role': 'user', 'content': new_message}]
        )

        #merging past messages with current to conserve history
        messages += [
            {'role': 'user', 'content': new_message},
            {'role': 'assistant', 'content': chat_response.message.content}
            ]
        print(chat_response.message.content + '\n')
    except queue.Empty:
        continue



stop_listening(wait_for_stop=False)