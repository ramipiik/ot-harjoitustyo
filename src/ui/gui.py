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

        heading1_label = ttk.Label(master=self._root, text="Kirjaudu", font=("Arial", 20))
        heading1_label.grid(row=0, column=0, padx=5, pady=10, sticky=(constants.W), columnspan=2)

        username1_label = ttk.Label(master=self._root, text="Käyttäjänimi")
        username1_label.grid(row=1, column=0, padx=5, pady=5,sticky=(constants.W))
        
        self.username_entry1 = ttk.Entry(master=self._root)
        self.username_entry1.grid(row=1, column=1, sticky=(constants.W, constants.E), padx=5, pady=5)
        
        password_label1 = ttk.Label(master=self._root, text="Salasana")
        password_label1.grid(row=2, column=0, padx=5, pady=5, sticky=(constants.W))
        
        self.password_entry1 = ttk.Entry(master=self._root)
        self.password_entry1.grid(row=2, column=1, sticky=(constants.W, constants.E), padx=5, pady=5)
        
        login_button = ttk.Button(
            master=self._root,
            text="Kirjaudu",
            command=self._handle_login_click
            )
        login_button.grid(row=4, column=0, sticky=(constants.W, constants.E), padx=5, pady=5, columnspan=2)
        

        heading2_label = ttk.Label(master=self._root, text="Luo uusi käyttäjä", font=("Arial", 20))
        heading2_label.grid(row=0, column=2, padx=(50,5), pady=10, sticky=(constants.W), columnspan=2)

        username_label2 = ttk.Label(master=self._root, text="Käyttäjänimi")
        username_label2.grid(row=1, column=2, padx=(50,5), pady=5, sticky=(constants.W))
        
        self.username_entry2 = ttk.Entry(master=self._root)
        self.username_entry2.grid(row=1, column=3, sticky=(constants.W, constants.E), padx=5, pady=5)
        
        password_label2 = ttk.Label(master=self._root, text="Salasana")
        password_label2.grid(row=2, column=2, padx=(50,5), pady=5, sticky=(constants.W))

        self.password_entry2 = ttk.Entry(master=self._root)
        self.password_entry2.grid(row=2, column=3, sticky=(constants.W, constants.E), padx=5, pady=5)

        password_label3 = ttk.Label(master=self._root, text="Salasana uudestaan")
        password_label3.grid(row=3, column=2, padx=(50,5), pady=5, sticky=(constants.W))
        
        self.password_entry3 = ttk.Entry(master=self._root)
        self.password_entry3.grid(row=3, column=3, sticky=(constants.W, constants.E), padx=5, pady=5)
        
        signup_button = ttk.Button(
            master=self._root,
            text="Luo käyttäjä",
            command=self._handle_signup_click
            )
        signup_button.grid(row=4, column=2, sticky=(constants.W, constants.E), padx=(50,5), columnspan=2, pady=5)
        
    
        self._root.grid_columnconfigure(1, weight=1, minsize=200)
        self._root.grid_columnconfigure(3, weight=1, minsize=200)


    def _handle_login_click(self):
        #To-do: Lisää virheidenkäsittely
        username_value1 = self.username_entry1.get()
        password_value1 = self.password_entry1.get()
        user = login(username_value1, password_value1)
        portfolios_UI(self, user)
    
    def _handle_signup_click(self):
        #To-do: Tarkista 2. salasana
        #To-do: Lisää virheidenkäsittely
        username_value2 = self.username_entry2.get()
        password_value2 = self.password_entry2.get()
        user=signup(username_value2, password_value2)
        portfolios_UI(self, user)