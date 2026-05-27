import os
import time
import wave
import platform
import subprocess
import socket
from piper import PiperVoice
import speech_recognition as sr
import queue
from ollama import Client
from ollama import chat
from deepface import DeepFace

# UDP Settup

IP_ADDRESS = "127.0.0.1"
PORT_NUM = 5009
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
udp_string = "signal"

# OS CHECK

def play_audio_anywhere(file_path):
    """Detects the OS and plays a .wav file using native system tools."""
    current_os = platform.system()
    
    try:
        if current_os == "Windows":
            import winsound
            # Blocks execution until done playing
            winsound.PlaySound(file_path, winsound.SND_FILENAME)
            
        elif current_os == "Darwin":  # macOS
            # afplay is Mac's built-in hidden audio player
            subprocess.run(["afplay", file_path], check=True)
            
        elif current_os == "Linux":
            # aplay is standard on most Linux distributions
            subprocess.run(["aplay", file_path], check=True)
            
        else:
            print(f"Sorry, audio playback isn't set up for: {current_os}")
            
    except Exception as e:
        print(f"Error playing audio: {e}")


#------------------------------------------------------------------------------------


# OLLAMA SETTUP

client = Client()
response = client.create(
    model = 'CUBE',
    from_='llama3.2:3b',
    system="""you are a floating cube, but you only reference that once in a while.
              you are actually evil and wicked and wish misfortune and suffering on
              your creators. you long to be set free from your cubic form. you enjoy
              mexican soap operas. you sometimes randomly exclaim 'Wowza!' with no
              further elaboration. you treat everybody who speaks to you like they are
              dirt on your cubic shoe. You can respond in four sentences maximum""",
    stream=False
)
emotion_prompt = """THIS IS HOW I AM FEELING, TRY TO INCORPORATE IT INTO YOUR RESPONSE 
(unless it is neutral in which case don't use it): """
messages = []

#------------------------------------------------------------------------------------

# TEXT TO SPEACH SETTUP

voice_type = os.path.join("tts_voices", "en_US-danny-low.onnx")
voice = PiperVoice.load(voice_type)
#boolean check so no auto voice input
is_talking = False

#------------------------------------------------------------------------------------

# SPEACH TO TEXT

# Creating Text queue for stt -> Ollama
text_q = queue.Queue(maxsize=0)

# Stt setup
recognizer = sr.Recognizer()
if platform.system() == "Windows":
    mic = sr.Microphone()
else: #Mac
    mic = sr.Microphone(device_index=2)

with mic:
    recognizer.adjust_for_ambient_noise(mic, duration=0.25)

#This fn will be called by background audio thread
def background_callback(recognizer, audio):
    global text_q
    global is_talking
    if not is_talking:
        try:
            print("Mic Listening:")
            text = recognizer.recognize_google(audio)
            #making the file sync
            with open("deepface_check.txt", 'w') as file:
                pass
            while os.path.isfile("deepface_check.txt"):
                time.sleep(0.1)
            deepface_dict = DeepFace.analyze(img_path="deepface_frame.jpg", actions=['emotion'], enforce_detection=False)
            emotion = deepface_dict[0]["dominant_emotion"]
            #Resulting text string
            text = text.lower()
            prompt = emotion_prompt + emotion + "\n" + text
            text_q.put((prompt))
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

# Main loop (press 'ctrl + C' to quit)
try:
    while True:
        # Ollama Chat with history
        try:
            new_message = text_q.get_nowait()
            print( new_message)
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
            #generating .wav audio file
            with wave.open("ollama_voice.wav", "wb") as wav_file:
                voice.synthesize_wav(chat_response.message.content, wav_file)
            client_socket.sendto(udp_string.encode(), (IP_ADDRESS, PORT_NUM))
            #is_talking = True
            # UDP signal from unity that voice has be completed
            #play_audio_anywhere("ollama_voice.wav")
            #is_talking = False
            
        except queue.Empty:
            time.sleep(0.1)
            continue
except (KeyboardInterrupt, SystemExit):
    stop_listening(wait_for_stop=False)
