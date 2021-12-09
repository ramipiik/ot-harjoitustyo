from tkinter import StringVar, Tk, constants, ttk
from services.user_services import login, signup
from ui.text_ui import portfolios_UI

class UI:
    def __init__(self, root):
        self._root = root
        self._current_view=None
        self._username=None
        self._frame = None
        self._initialize()


    def _initialize(self):
        self._frame = ttk.Frame(master=self._root)


    def start(self):
        username_label = ttk.Label(master=self._root, text="Username")
        self.username_entry = ttk.Entry(master=self._root)
        password_label = ttk.Label(master=self._root, text="Password")
        self.password_entry = ttk.Entry(master=self._root)
        login_button = ttk.Button(
            master=self._root,
            text="Login",
            command=self._handle_login_click
            )
        username_label.grid(padx=5, pady=5)
        self.username_entry.grid(row=0, column=1, sticky=(constants.E, constants.W), padx=5, pady=5)
        password_label.grid(padx=5, pady=5)
        self.password_entry.grid(row=1, column=1, sticky=(constants.E, constants.W), padx=5, pady=5)
        login_button.grid(columnspan=2, sticky=(constants.E, constants.W), padx=5, pady=5)
        self._root.grid_columnconfigure(1, weight=1, minsize=300)
   

    def _handle_login_click(self):
        username_value = self.username_entry.get()
        password_value = self.password_entry.get()
        user = login(username_value, password_value)
        self._frame.quit()
        portfolios_UI(self, user)     