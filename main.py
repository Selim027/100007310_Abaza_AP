import tkinter as tk
from hmi import MarkerHMI

if __name__ == "__main__":
    root = tk.Tk()
    app = MarkerHMI(root)
    root.mainloop()
