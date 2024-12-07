from enum import Enum
import tkinter as tk
from tkinter import scrolledtext
from datetime import datetime

class LogLevel(Enum):
    NOTSET = 0
    DEBUG = 10
    INFO = 20
    ERROR = 40


class Logger:

    txtLog: scrolledtext.ScrolledText = None
    level = LogLevel.INFO

    def SetTextLog(obj):
        Logger.txtLog = obj
        Logger.txtLog.tag_config('prefix', foreground='#3d6cd1')
        Logger.txtLog.tag_config('error', foreground='#c73030')
        Logger.txtLog.tag_config('darkgrey', foreground='#595959')

    def log(msg:str, level: LogLevel = LogLevel.NOTSET):
        if level.value != LogLevel.NOTSET.value and level.value < Logger.level.value:
            return
        match(level):
            case LogLevel.ERROR:
                tag = "error"
            case LogLevel.DEBUG:
                tag = "darkgrey"
            case _:
                tag = ""
        scrollDown = True if (Logger.txtLog.yview()[1] > 0.8) else False
        Logger.txtLog.configure(state='normal')
        Logger.txtLog.insert(tk.END, f"{datetime.now().strftime('[%x %X]:')} ", "prefix")
        Logger.txtLog.insert(tk.END, f"{msg}\n", tag)
        Logger.txtLog.configure(state='disabled')
        if scrollDown:
            Logger.txtLog.see(tk.END)

    def info(msg):
        Logger.log(msg, LogLevel.INFO)

    def error(msg):
        Logger.log(msg, LogLevel.ERROR)

    def debug(msg):
        Logger.log(msg, LogLevel.DEBUG)