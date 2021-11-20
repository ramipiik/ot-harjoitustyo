from repositories.user_repository import verify_user, store_user
from ui.styles import bcolors


def login(username, password):
    """Service for logging in a user"""
    response = verify_user(username, password)
    # To do: Move prints to text_ui?
    if response:
        print(f"{bcolors.OKCYAN}{username} logged in")
        print(f"--------------------{bcolors.ENDC}")
        return username
    else:
        print(f"{bcolors.FAIL}--------------------")
        print(f"User not found or incorrect password")
        print(f"--------------------{bcolors.ENDC}")
        return None


def logout():
    # To be done
    pass


def signup(username, password):
    """Service for signing up a new user"""
    response = store_user(username, password)
    # To do: Move prints to text_ui?
    if response:
        print(f"{bcolors.OKCYAN}--------------------")
        print(f"{username} created")
        print(f"--------------------{bcolors.ENDC}")
        return verify_user(username, password)
    else:
        return False
