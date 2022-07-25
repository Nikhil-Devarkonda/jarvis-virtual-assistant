import time

s = time.time()
print("[Loding Jarvis.py]")
# Process 
from threading import Thread
import Process
def th():
    Process.init()
Thread(target=th).start()
print("[Loaded Process.py]")
from Classifer import intentClassifier
print("[Loaded Classifer.py]")
from Speech import listen
print("[Loaded Speech.py]")
from voice import Speak,outputQueue
import utils.Config as Config
print("Process took ",(time.time()-s))

print(f"\n[Jarvis Ready]\n")


class Jarvis:
    def __init__(self):
        self.process = Process.Process()
        self.classify = intentClassifier  # Function
        self.context = {}                 # Format of Context -> [ { 'set_context': "intent_name" , "entities":{}" } , ......]
        
        
    def start(self):
        Speak("Jarvis at your service sir")
        Config.set("INPUT MODE","TEXT")
        while True:
                # if(Process.Event.isOnline()):
                #     text = listen('online')
                # else:
                    # text = listen('text')
                # text = listen('text')    
                text = listen()
                # Set the mode of input to jarvis
                if "firebase mode"==text:
                    Speak("Switching to Firebase mode")
                    Config.set("INPUT MODE","FIREBASE")
                    continue
                if(text=="listening mode"):
                    mode = 'listening'
                    Config.set("INPUT MODE","LISTENING")
                    continue
                if(text=="text mode"):
                    Speak("Switching to text mode")
                    Config.set("INPUT MODE","TEXT")
                    mode = 'text'
                    continue
                if text == "ERROR" :
                    
                    Speak("Sir i am unable to hear you") 
                if text == None :
                    # print("Retrying for firebase")
                    continue
                if text == "exit" or text=="bye":
                   break 
                else:    
                    # print(text)
                        intent,self.context = self.classify(text,self.context)
                        print(intent,self.context)
                        if intent == None:
                            Speak("Unable to understand what you said")
                        else:
                            try:     
                                self.process.start(intent,text)
                            except Exception as e:
                                Speak("i found an internal error in my system:")
                                print(e)




if __name__ == "__main__":
    # import os
    # os.system("cls")
    Process.init()
    # print("[Processes Started....]")
    # J = Jarvis()
    # print("[Jarvis Intialise.....]")
    print(outputQueue)
    input()
    # J.start()
    print("[Terminating.....]")
    Process.terminate()
    
    




            
            
