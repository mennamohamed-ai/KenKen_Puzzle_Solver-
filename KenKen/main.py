# main.py
# Entry point to launch the KenKen Tkinter GUI

from tkinter import Tk
from gui import KenKenGUI

def main():
    root = Tk()
    app = KenKenGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
