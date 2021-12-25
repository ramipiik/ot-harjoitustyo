from tkinter import Tk
from ui.gui.gui import GUI

window = Tk()
window.title("Sijoitussimulaattori")

gui = GUI(window)
gui.start()
window.mainloop()
