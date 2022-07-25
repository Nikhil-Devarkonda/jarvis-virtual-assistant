from threading import Thread
#Load Process--------------------------------------------------------------
def load_process():
    global Process
    import Process
    print("*[Process Module Loaded]")
T_P = Thread(target=load_process)
T_P.start()
#Load Classifier---------------------------------------------------------------
def load_classifer():
    global intentClassifier
    from Classifer import intentClassifier
    print("*[Classifier Loaded]")
T_C = Thread(target=load_classifer)
T_C.start()
#-----------------------------------------------------------------------------
from voice import Speak,output_queue
import utils.Config as Config
import utils.myfirebase as myfirebase
import playsound

# Load Activation Model in Background -------------------------------------
def load():
    global is_activated,activation_stream,activation_run
    from jarvis_activate import is_activated,stream,run
    activation_stream = stream
    activation_run = run
    print("*[Voice Activation Loaded]")
T = Thread(target=load)
T.start()




# Tkinter Modules :------------------------------------------------------
from tkinter import *
from tkinter.ttk import *
from tkinter.font import Font
from tkinter import Frame
import tkinter as tk
from PIL import Image, ImageTk
from Speech import *
import ast

T_P.join()


class Jarvis:
    class_thread_run = True
    is_process_over = True
    invoke_thread_pause = True
    firebase_on = False
    c = 0
    mode_no = 2
    def __init__(self):
        self.process = Process.Process()
        self.classify = intentClassifier  # Function
        self.context = {}                 # Format of Context -> [ { 'set_context': "intent_name" , "entities":{}" } , ......]
        self.master = Tk()
        self.master.title("Jarvis")
        # self.master.attributes("-topmost",True)
        self.master.configure(background='#000000')#0042ff
        # setting geometry of tk window
        self.master.geometry("900x500")
        self.titleFont = Font(family='algerian', size=36, weight='bold')
        self.textFont = Font(family='times new roman', size=20, weight='bold')
        self.setFont = Font(family='verdana', size=10)
        self.mainFrame = Frame(self.master, background='#000000', width=900, height=500)
        self.mainFrame.grid(row=0, column=0)
        #  Threads
        self.thread_firebase = Thread(target=self.firebase_thread)
        self.thread_out = Thread(target=self.output_thread)
        self.thread_activation = Thread(target=self.invoke_thread)
        self.thread_firebase.name = "Firebase"
        self.thread_activation.name = "Activation"
        self.thread_out.name = "Output"
    # Main Window ---------------------------------------------------------

    def createGUI(self):
        #---------- Main GUI ----------#
        self.img = Image.open("arc_reactor.png").resize((290, 290))
        self.display = ImageTk.PhotoImage(self.img)

        self.logo = Label(self.mainFrame, image=self.display, width=100, background='black')
        self.logo.place(relx=1, x=-870, y=130)
        self.logo.bind("<Button-1>", lambda event: self.show())

        #---------- Settings ICON  ----------#
        self.setting_icon = ImageTk.PhotoImage(Image.open("assets/setting_icon.png").resize((50, 50)))
        self.settings = Label(self.mainFrame, width=5, background="black")
        self.settings.place(relx=1, x=-65, y=10)
        self.settings.bind("<Button-1>", lambda event: self.show_settings())
        self.settings['image']=self.setting_icon

        #----------- Title ------------------
        self.title = tk.Label(self.mainFrame, text="Jarvis", font=self.titleFont,fg="blue",background="black")
        self.title.place(relx=1, x=-565, y=20)
        
        self.input = Entry(self.mainFrame, font=self.textFont, width=24)
        # self.input.bind("<FocusIn>", self.show)
        #------------ Input Box --------------#
        self.input.place(relx=1, x=-565, y=370)
        self.input.bind("<Return>", (lambda event: self.runCommand()))
        self.input.insert(INSERT, "Command")

        #------------ Output Box --------------#
        self.output = Text(self.mainFrame, height=11, width=47, font=self.setFont, background='black',fg='#34b4eb')
        self.scr = Scrollbar(self.mainFrame)
        self.scr.config(command=self.output.yview)
        self.output.config(yscrollcommand=self.scr.set)
        self.output.insert(INSERT, "[Jarvis on Service]\n")
        self.output.configure(state="normal")
        self.output.bind("<1>", lambda event: self.output.focus_set())
        # scr.place(relx=1, x=-380, y=290)
        self.output.place(relx=1, x=-565, y=130)
        

        # Icons [ Mode ]
        self.microphone_icon = ImageTk.PhotoImage(Image.open("assets/microphone_icon.png").resize((50, 50))) 
        self.text_mode_icon = ImageTk.PhotoImage(Image.open("assets/text_mode_icon.png").resize((54, 54)))
        self.firebase_icon = ImageTk.PhotoImage(Image.open("assets/firebase_icon.png").resize((60, 60)))
        self.processing_icon = ImageTk.PhotoImage(Image.open("assets/processing_icon.png").resize((54, 54)))
        
        self.mode = Label(self.mainFrame, font=self.textFont, width=4, background='black')
        self.mode.bind("<Button-1>", lambda event: self.switch_mode())
        self.mode.place(relx=1, x=-150, y=360)
        self.mode['image'] = self.text_mode_icon
        
        input_mode['textbox'] = self.input
        # Thread Starts Here :
        self.thread_out.start()
        time.sleep(1)
        self.thread_activation.start()
        self.thread_firebase.start()
        time.sleep(1)
        self.master.mainloop()
        self.on_close()       
    def show(self):
        # print("Hello")

        if Jarvis.c % 2 == 0:
            self.logo['background'] = "black"
            self.mode['image'] = self.firebase_icon
        elif Jarvis.c % 3 == 0:
            self.mode['image'] = self.text_mode_icon
        else:
            self.mode['image'] = self.microphone_icon
            self.logo['background'] = "#00f7ff"
        
        Jarvis.c += 1
        # self.settings['image'] = self.display
    def switch_mode(self):
        print(self.mode_no)    
        # TEXT
        if self.mode_no == 1:
            utils.Config.set("INPUT MODE","TEXT")
            self.mode['image']=self.text_mode_icon
            self.invoke_thread_pause = True
            activation_run[0]=False
            self.firebase_on = False
            Speak("Switching to text mode")
        # LISTENING
        if self.mode_no == 2:
            if Process.Event.isOnline(speak=False) :
                self.firebase_on = False
                self.invoke_thread_pause = False
                utils.Config.set("INPUT MODE","LISTENING")
                self.mode['image']=self.microphone_icon
                Speak("Switching to listening mode")
            else:
                Speak("Sir Need Internet Connection to Switch into Listening mode")
        # FIREBASE
        if self.mode_no == 3:
            if Process.Event.isOnline(speak=False) :
                activation_run[0] = False
                self.firebase_on = True
                self.invoke_thread_pause = True
                utils.Config.set("INPUT MODE","FIREBASE")
                self.mode['image']=self.firebase_icon
                Speak("Switching to firebase mode")
            else:
                Speak("Sir Need Internet Connection to Switch into Firebase mode")
        
        self.mode_no = self.mode_no  + 1
        if self.mode_no > 3 :
            self.mode_no = 1

    # Settings ------------------------------------------------------------

    def show_settings(self):
        # Load Data
        f = open("utils/config.json")
        data = f.read()
        config = utils.Config.get_json_dict()
        # frame.tkraise()
        self.win = tk.Toplevel(self.master)
        self.win.title('Settings')
        self.win.geometry("715x500")
        self.win.configure(background='black')
        self.settingsFrame = Frame(self.win, background='black', height=500)
        self.settingsFrame.pack()
        self.canvas = tk.Canvas(self.settingsFrame, width=690, height=500, bg='black')
        self.scrollbar = tk.Scrollbar(self.settingsFrame, orient="vertical", command=self.canvas.yview, width=40)
        self.scrollable_frame = tk.Frame(self.canvas, bg='black')
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            )
        )
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor='nw')
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.canvas.pack(side="left")
        self.scrollbar.pack(side="right", fill="y")
        # Get Reference Dictionary[Objects]   |  Add Components to Settings
        self.ref_dict = self.addWidget(config,dict())
        # Save Button
        self.add(value="Save",type_="btn")  
    def addWidget(self,config,ref_dict):
        for i in config:
            if isinstance(config[i],dict):
                # At title :
                frame = tk.Frame(master=self.scrollable_frame, bg='blue', width=900, height=500)
                title = lbl = tk.Label(master=frame,text=i, bg='blue', font=self.setFont,fg='white')
                lbl.pack(side=tk.LEFT)
                frame.pack()
                # Create new ref_dict for nesting
                ref_dict[i] = self.addWidget(config[i],dict())
                continue
            if isinstance(config[i],bool):
                ty = 'checkbox'
            else:
                ty = 'text'
            ref_dict[i]=self.add(i,config[i],ty)
        return ref_dict
    def add(self, key="", value="", type_='text'):
        frame = tk.Frame(master=self.scrollable_frame, bg='black', width=900, height=500)
        ref = None
        if type_ == 'text':
            lbl = tk.Label(master=frame,text=key+" : ",justify="left", width=30, font=self.setFont,fg='white',bg='black')
            lbl.pack(side=tk.LEFT)
            ent = None
            if key.endswith("PWD"):
                ent = tk.Entry(master=frame, width=30, bg='white', font=self.setFont,show="*")
            else:
                ent = tk.Entry(master=frame, width=30, bg='white', font=self.setFont)
            ent.insert(tk.INSERT, value)
            ent.pack(side=tk.RIGHT)
            ref = ent
        if type_ == 'checkbox':
            # create checkbox.
            chk = tk.Checkbutton(master=frame, text=key, bg='black', font=self.setFont,fg='white')
            if value == True:
                chk.select()
            else:
                chk.deselect()
            chk.pack(side=tk.RIGHT)
            ref = chk
        if type_=='btn':
            btn = tk.Button(master=frame, text=value, font=self.setFont, command=lambda: self.saveSettings())
            btn.pack()
        frame.pack()
        return ref
    def save_to_config(self,ref_dict):
        # Uses recursion
        for i in ref_dict:
            if  isinstance(ref_dict[i],dict):
                ref_dict[i]=self.save_to_config(ref_dict[i])
            if isinstance(ref_dict[i],tk.Entry):
                ref_dict[i]= ref_dict[i].get() 
            if isinstance(ref_dict[i],tk.Checkbutton):
                ref_dict[i]=ref_dict[i].state()
        return ref_dict
    def saveSettings(self):
        # Use ref_dict 
        c = self.save_to_config(self.ref_dict)
        # Printing
        for i in c:
            print(i,"->",c[i])
        # Writing to file
        utils.Config.write_to_json(c)
        Speak("Settings Saved")
    
    # Executions -----------------------------------------------------------   

    def execute_command(self,text):
        # if 'firebase' in text.lower():
        #     Config.set('INPUT MODE','FIREBASE')
        #     Config.set('FIREBASE','ON')
        #     self.firebase_on = True
        #     Speak("Firebase mode Activated")
        #     return
        self.input.delete("0","end")
        if self.is_process_over :
        #    self.process_thread(text) 
           p =  Thread(target=self.process_thread,args=[text])
           p.name = "Processsing"
           p.start()
    def runCommand(self):
        text = self.input.get()
        if input_mode['type']=='entity':
                input_mode['output'] = text
        if self.is_process_over :
            if input_mode['type']=='command':
                self.execute_command(text)
        # self.input.insert()   
    def output_thread(self):
        import time
        time.sleep(2)
        try:
            # self.output.delete("1.0","end")
            while self.class_thread_run:
                if output_queue==[]:
                    continue           
                self.output.see("end")
                self.output.insert(INSERT, "Jarvis : "+output_queue[0]+"\n")
                if self.firebase_on:
                    myfirebase.append_chat(output_queue[0]+"\n")
                output_queue.pop(0)
        except:
            pass
    def firebase_thread(self):
        timeout = 5
        while self.class_thread_run:
            time.sleep(1)
            if self.firebase_on==True and self.is_process_over: 
                msg = myfirebase.get_last_chat()
                if msg == None:
                        continue
                if input_mode['type']=='entity':
                        input_mode['ouput'] = msg
                if input_mode['type']=='command':
                        self.execute_command(msg)
                myfirebase.append_chat("#")
    def process_thread(self,text):  
        # Set few thnigs
        self.pervious_mode = self.mode['image']
        self.mode['image'] = self.processing_icon
        self.is_process_over = False
        self.output.insert(END, "You    : "+text+"\n")
        self.input.config(state='disable')
        # Intent Classification and Execution
        print('Processing-------------------------------------------------')
        intent, self.context = self.classify(text, self.context)
        # print(intent, self.context)
        if intent == None:
            Speak("Unable to understand what u said")
        else:
            try:
                out = self.process.start(intent, text)
                self.input.delete(0, 'end')
                # self.set(out)
                # Speak(out)
                pass
            except Exception as e:
                Speak("i found an internal error in my system:")
                print(e) 
        print('-----------------------------------------------------------')
        # Reset back
        self.is_process_over = True
        self.mode['image'] = self.pervious_mode
        self.input.config(state='enable')
    def invoke_thread(self):
        global T
        T.join()
        while self.class_thread_run:
            if self.is_process_over == False or self.invoke_thread_pause:
                time.sleep(1)
                print("#")
                continue
            elif is_activated() :
                # Code for Listening..... Here [Add it]
                playsound.playsound("assets/wake_sound.mp3")
                Speak("Yes Sir")
                self.execute_command(listen('LISTENING'))
    def on_close(self):
        try:
            # Stop Threads         
            self.class_thread_run = False
            # Reset Input Mode to Text
            utils.Config.set("INPUT MODE","TEXT")
            utils.Config.set("FIREBASE","OFF")
            activation_run[0]= False
        except:
            pass
     
        
if __name__ == "__main__":
    Process.init()
    J = Jarvis()
    J.createGUI()
    Process.terminate()

