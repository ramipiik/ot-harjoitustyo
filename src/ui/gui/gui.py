from ui.gui.practise_view import TestView
from ui.gui.login_view import LoginView


class GUI:
    """Class for creating the GUI"""

    def __init__(self, root):
        self._root = root
        self._current_view = None

    def start(self):
        """Shows the initial view"""
        self._show_login_view()

    def _hide_current_view(self):
        """Hides the current view"""
        if self._current_view:
            self._current_view.destroy()
        self._current_view = None

    def _show_test_view(self):
        """Hides the current view and shows test view"""
        self._hide_current_view()
        self._current_view = TestView(self._root, self._show_login_view)
        self._current_view.grid()

    def _show_login_view(self):
        """Hides the current view and shows login view"""
        self._hide_current_view()
        self._current_view = LoginView(self._root, self._show_test_view)
        self._current_view.grid()
