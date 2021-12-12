from ui.text_ui import start
from tkinter import Tk
from ui.gui import GUI

window = Tk()
window.title("Sijoitussimulaattori")

gui = GUI(window)
gui.start()
window.mainloop()

#Starts the text-ui
# start()