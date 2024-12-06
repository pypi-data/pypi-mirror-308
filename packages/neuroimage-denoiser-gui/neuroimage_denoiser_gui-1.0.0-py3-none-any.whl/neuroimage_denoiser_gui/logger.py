import tkinter as tk
from tkinter import scrolledtext
from datetime import datetime

class Logger:

    txtLog: scrolledtext.ScrolledText = None

    def SetTextLog(obj):
        Logger.txtLog = obj
        Logger.txtLog.tag_config('prefix', foreground='#3d6cd1')
        Logger.txtLog.tag_config('error', foreground='#c73030')

    def _log(msg:str, tag:str=""):
        scrollDown = True if (Logger.txtLog.yview()[1] > 0.8) else False
        Logger.txtLog.configure(state='normal')
        Logger.txtLog.insert(tk.END, f"{datetime.now().strftime('[%x %X]:')} ", "prefix")
        Logger.txtLog.insert(tk.END, f"{msg}\n", tag)
        Logger.txtLog.configure(state='disabled')
        if scrollDown:
            Logger.txtLog.see(tk.END)

    def info(msg):
        Logger._log(msg)

    def error(msg):
        Logger._log(msg, "error")