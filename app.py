import tkinter as tk
from tkinter import filedialog
from core.builder import build
from core.logger import log_queue
import threading
class App(tk.Tk):
 def __init__(s):super().__init__();s.title('ISO Studio CAOS');s.geometry('700x400');s.k=tk.StringVar();s.i=tk.StringVar();s.r=tk.StringVar();tk.Button(s,text='Kernel',command=lambda:s.k.set(filedialog.askopenfilename())).pack();tk.Button(s,text='RootFS',command=lambda:s.r.set(filedialog.askdirectory())).pack();tk.Button(s,text='BUILD',command=lambda:threading.Thread(target=build,args=({'kernel':s.k.get(),'rootfs':s.r.get(),'output':'enzo.iso'},),daemon=True).start()).pack();s.t=tk.Text(s,bg='black',fg='lime');s.t.pack(fill='both',expand=True);s.after(100,s.u)
 def u(s):
  while not log_queue.empty():s.t.insert('end',log_queue.get()+'\n');s.t.see('end');s.after(100,s.u)
