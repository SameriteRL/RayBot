from typing import Callable
from tkinter import *
from tkinter import ttk
import ui.customtk as customtk
from globals import *

class RayBotUI(customtk.TkWindow):
    def __init__(self, killcmd:Callable):
        super().__init__(
            title="RayBot",
            geometry="300x100",
            centerscreen=True,
            includeframe=True
        )
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        self.kill_button = ttk.Button(
            self.mainframe,
            text="Kill bot",
            command=killcmd
        )
        self.kill_button.grid(column=0, row=0)
        self.mainframe.rowconfigure(0, weight=1)
        self.mainframe.columnconfigure(0, weight=1)