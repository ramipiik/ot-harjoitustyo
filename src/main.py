from tkinter import Tk

# from ui.text_ui.text_ui import start_UI
from ui.gui.gui import GUI

window = Tk()
window.title("Sijoitussimulaattori")

gui = GUI(window)
gui.start()
window.mainloop()

# Starts the text-ui
# start_UI()
