# Requires PyAudio and PySpeech.
import speech_recognition as sr
from voice import Speak
import time
import utils.Config as Config
# Record Audio
# Gobals :
input_mode = {'type':'command','output':None,'textbox':None}
r = sr.Recognizer()


def listen(mode="",entity_mode=False):
    global input_mode
    if mode=="":
        mode = Config.get("INPUT MODE")
    # Clear the text box
    input_mode['textbox'].config(state="enable")
    if input_mode['textbox']!=None:
        input_mode['textbox'].insert('insert',"")

    if mode=="TEXT":
        if entity_mode==True:
            input_mode['type']='entity'
            input_mode['output']=None
            while input_mode['output']==None:
                pass
            input_mode['type']='command'
            return input_mode['output']
    if mode=="FIREBASE":
        Config.set("FIREBASE","ON")
        if entity_mode==True:
            input_mode['type']='entity'
            input_mode['output']=None
            while input_mode['output']==None:
                pass
            input_mode['type']='command'
            return input_mode['output'] 
    if mode=="LISTENING":
        # Speech recognition using Google Speech Recognition
        try:
            # for testing purposes, we're just using the default API key
            # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
            # instead of `r.recognize_google(audio)`
            with sr.Microphone() as source:
                print("Listening...")
                audio = r.listen(source,timeout=5,phrase_time_limit=5)
            print(r.recognize_google(audio))
            return r.recognize_google(audio)
        except sr.UnknownValueError:
            # Speak("Google Speech Recognition could not understand audio")
            return ""
        except sr.RequestError as e:
            Speak("Could not request results from Google Speech Recognition service; {0}".format(e))
            return ""
# def set_input_source(src):
#     global input_box
#     print(src)
#     input_box = src
#     print("Source Set")
if __name__ == "__main__":
    print(listen(mode="LISTENING"))