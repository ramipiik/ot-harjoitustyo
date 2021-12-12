from tkinter import constants, ttk

class TestView:
    """Class for testing and trying out stuff"""
    def __init__(self, root, show_login_view):
        self._root = root
        self._current_view=None
        self._frame = None
        # self._switch_to_login_view = switch_to_login_view
        self._show_login_view = show_login_view
        self._initialize()

    def destroy(self):
        """Destroys current frame"""
        self._frame.destroy()
    
    def _initialize(self):
        """Initializes the TestView object"""
        self._frame = ttk.Frame(master=self._root)
        label = ttk.Label(master=self._frame, text="Hello!")
        
        button = ttk.Button(
            master=self._frame,
            text="Back to login page",
            command=self._show_login_view
        )

        label.grid(row=0, column=0)
        button.grid(row=2, column=0, pady=(40,20), columnspan=2, rowspan=2, sticky=(constants.W, constants.E))
    
    def grid(self):
        """Plots the frame as grid"""
        self._frame.grid(columnspan=4, padx=10, pady=10)
