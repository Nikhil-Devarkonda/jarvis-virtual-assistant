import tkinter as tk
import tkinter.font as tkFont
window = tk.Tk()
window.geometry("500x344+1030+450")
fontStyle = tkFont.Font(family="Lucida Grande", size=16)

ent_to = tk.Entry(font=fontStyle)
ent_to.insert(tk.INSERT,"To:")
ent_to.pack(fill=tk.X)

ent_subject = tk.Entry(font=fontStyle)
ent_subject.insert(tk.INSERT,"Subject:")
ent_subject.pack(fill=tk.X)

txt_msg = tk.Text(font=fontStyle,height=10)
txt_msg.pack(fill=tk.X)

btn = tk.Button(text='Send',font=fontStyle)
btn.pack(side=tk.LEFT)


def show_window():
    window.mainloop()

from threading import Thread
show_window()
# Thread(target=show_window).start()

print("Working")
