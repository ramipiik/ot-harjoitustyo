from ui.text_ui import start
from tkinter import Tk
from ui.gui import UI

window = Tk()
window.title("Sijoitussimulaattori")

gui = UI(window)
gui.start()
window.mainloop()