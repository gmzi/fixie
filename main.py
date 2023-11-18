import tkinter as tk
import tkinter.ttk as ttk

window = tk.Tk()

frame1 = tk.Frame(master=window, width=200, height=100, bg="red")
frame1.pack(fill=tk.BOTH, side=tk.LEFT, expand=True)

frame2 = tk.Frame(master=window, width=100, bg="yellow")
frame2.pack(fill=tk.BOTH, side=tk.LEFT, expand=True)

frame3 = tk.Frame(master=window, width=50, bg="blue")
frame3.pack(fill=tk.BOTH, side=tk.LEFT, expand=True)

# label = ttk.Label(text="hello ttk")
label = tk.Label(
    master=frame1,
    text="I'm at (0, 0)",
    foreground="white",
    background="#34A2FE",
    width=10,
    height=3
    )
label.place(x=10, y=10)

label1 = tk.Label(
    master=frame1,
    text="I'm at (75, 75)",
    foreground="white",
    background="#34A2FE",
    width=10,
    height=3
    )
label1.place(x=75, y=75)

button = ttk.Button(
    master=frame2,
    text="Click me!",
    command=lambda: print("clicked"),
    style="TButton"
).pack()

for i in range(3):
    window.columnconfigure(i, weight=1, minsize=75)
    window.rowconfigure(i, weight=1, minsize=50)

    for j in range(0, 3):
        frame = tk.Frame(
            master=frame3,
            relief=tk.RAISED,
            borderwidth=1
        )
        frame.grid(row=i, column=j, padx=5, pady=5)
        label = tk.Label(master=frame, text=f"Row {i}\nColumn {j}")
        label.pack(padx=5, pady=5)

# frame.pack()

def handle_keypress(event):
    print(event.char)

# Bind keypress event to handle_keypress()
window.bind("<Key>", handle_keypress)

window.mainloop()
