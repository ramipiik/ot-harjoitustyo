from tkinter import StringVar, constants, ttk
from services.user_services import login, signup
from ui.text_ui.text_ui import open_portfolio_UI


class LoginView:
    """Creates the view for logging in and signing up"""
    def __init__(self, root, show_hello_view):
        self._root = root
        self._current_view=None
        self._frame = None
        self._show_hello_view=show_hello_view
        self._error_var1 = None
        self._error_var2 = None
        self._initialize()

    def destroy(self):
        """Destroys current frame"""
        self._frame.destroy()


    def grid(self):
        """Plots the frame as grid"""
        self._frame.grid(columnspan=4, padx=10, pady=10)


    def _initialize(self):
        """Initializes the TestView object"""
        self._frame = ttk.Frame(master=self._frame)
        self._error_var1=StringVar()
        self._error_var2=StringVar()

        self._error_label1 = ttk.Label(master=self._frame, textvariable=self._error_var1)
        self._error_label1.grid(row=5, column=0, sticky=(constants.W, constants.E), padx=5, pady=5, columnspan=2)

        self._error_label2 = ttk.Label(master=self._frame, textvariable=self._error_var2)
        self._error_label2.grid(row=5, column=2, sticky=(constants.W, constants.E), padx=(50,5), pady=5, columnspan=2)

        heading1_label = ttk.Label(master=self._frame, text="Kirjaudu", font=("Arial", 20))
        heading1_label.grid(row=0, column=0, padx=5, pady=10, sticky=(constants.W), columnspan=2)

        username1_label = ttk.Label(master=self._frame, text="Käyttäjänimi")
        username1_label.grid(row=1, column=0, padx=5, pady=5,sticky=(constants.W))
        
        self.username_entry1 = ttk.Entry(master=self._frame)
        self.username_entry1.grid(row=1, column=1, sticky=(constants.W, constants.E), padx=5, pady=5)
        
        password_label1 = ttk.Label(master=self._frame, text="Salasana")
        password_label1.grid(row=2, column=0, padx=5, pady=5, sticky=(constants.W))
        
        self.password_entry1 = ttk.Entry(master=self._frame, show = '*')
        self.password_entry1.grid(row=2, column=1, sticky=(constants.W, constants.E), padx=5, pady=5)
        
        login_button = ttk.Button(
            master=self._frame,
            text="Kirjaudu",
            command=self._handle_login_click
            )
        login_button.grid(row=4, column=0, sticky=(constants.W, constants.E), padx=5, pady=5, columnspan=2)

        heading2_label = ttk.Label(master=self._frame, text="Luo uusi käyttäjä", font=("Arial", 20))
        heading2_label.grid(row=0, column=2, padx=(50,5), pady=10, sticky=(constants.W), columnspan=2)

        username_label2 = ttk.Label(master=self._frame, text="Käyttäjänimi")
        username_label2.grid(row=1, column=2, padx=(50,5), pady=5, sticky=(constants.W))
        
        self.username_entry2 = ttk.Entry(master=self._frame)
        self.username_entry2.grid(row=1, column=3, sticky=(constants.W, constants.E), padx=5, pady=5)
        
        password_label2 = ttk.Label(master=self._frame, text="Salasana")
        password_label2.grid(row=2, column=2, padx=(50,5), pady=5, sticky=(constants.W))

        self.password_entry2 = ttk.Entry(master=self._frame, show = '*')
        self.password_entry2.grid(row=2, column=3, sticky=(constants.W, constants.E), padx=5, pady=5)

        password_label3 = ttk.Label(master=self._frame, text="Salasana uudestaan")
        password_label3.grid(row=3, column=2, padx=(50,5), pady=5, sticky=(constants.W))
        
        self.password_entry3 = ttk.Entry(master=self._frame, show = '*')
        self.password_entry3.grid(row=3, column=3, sticky=(constants.W, constants.E), padx=5, pady=5)
        
        signup_button = ttk.Button(
            master=self._frame,
            text="Luo käyttäjä",
            command=self._handle_signup_click
            )
        signup_button.grid(row=4, column=2, sticky=(constants.W, constants.E), padx=(50,5), columnspan=2, pady=5)
        
        switch_button = ttk.Button(
            master=self._frame,
            text="To test page",
            command=self._show_hello_view
        )
        switch_button.grid(row=6, column=0, sticky=(constants.W, constants.E), padx=(5,5), columnspan=4, pady=(30,5))
    
        self._root.grid_columnconfigure(1, weight=1, minsize=200)
        self._root.grid_columnconfigure(3, weight=1, minsize=200)


    def _handle_login_click(self):
        """Handles login process by using backend services"""
        username_value1 = self.username_entry1.get()
        password_value1 = self.password_entry1.get()
        user = login(username_value1, password_value1)
        if user:
            self._error_var1.set("Kirjautuminen onnistui.\nVoit jatkaa sovelluksen käyttöä terminaalissa.\n(GUIn laajentaminen työn alla.)")
            self._error_label1.config(foreground="green")
            self._frame.update()
            open_portfolio_UI(user)
        else:
            self._error_var1.set("Kirjautuminen ei onnistunut.\nKäyttäjää ei löytynyt tai väärä salasana.")
            self._error_label1.config(foreground="red")
    
    def _handle_signup_click(self):
        """Handles signup process by using backend services"""
        username_value2 = self.username_entry2.get()
        password_value2 = self.password_entry2.get()
        password_value3 = self.password_entry3.get()
        if password_value2!=password_value3:
            self._error_var2.set("Salasanat eivät täsmää.")
            self._error_label2.config(foreground="red")
            return
        if signup(username_value2, password_value2): 
            user = login(username_value2, password_value2)
            self._error_var2.set("Käyttäjän luonti onnistui.\nVoit jatkaa sovelluksen käyttöä terminaalissa.\n(GUIn laajentaminen työn alla.)")
            self._error_label2.config(foreground="green")
            self._frame.update()
            open_portfolio_UI(user)
        else:
            self._error_var2.set("Käyttäjänimi on jo käytössä.")
            self._error_label2.config(foreground="red")
