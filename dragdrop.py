import tkinter as tk
import tkinter.dnd as dnd

class DragDropWindow(tk.Tk):
    def __init__(self):
        super().__init__()

        self.geometry("300x300")

        self.label = tk.Label(self, text="Drag a file here!")
        self.label.pack(fill=tk.BOTH, expand=1)

        self.drop_target_register(dnd.FILES)
        self.drop_target_bind(self.label, "<Drop>", self.handle_drop)

    def handle_drop(self, event):
        files = self.tk.splitlist(event.data)
        for file in files:
            print(file)
