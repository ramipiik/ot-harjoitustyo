from repositories.user_repository import verify_user, store_user
from services.portfolio_services import get_portfolios
from ui.styles import bcolors
from entities.user import User


def login(username, password):
    """Service for logging in a user.

        Args:
            username:str
            password:str

        Returns:
            user object if login successful.
            None if login not succesfull.
    """    
    response = verify_user(username, password)
    # To do: Move prints to text_ui?
    if response:
        user = User(response[0], response[1], response[2])
        portfolios = get_portfolios(user)
        user.portfolios = portfolios
        print(f"{bcolors.OKCYAN}{user.username} logged in")
        print(f"--------------------{bcolors.ENDC}")
        return user
    print(f"{bcolors.FAIL}--------------------")
    print(f"User not found or incorrect password")
    print(f"--------------------{bcolors.ENDC}")
    return None


def logout():
    # To be done
    pass


def signup(username, password):
    """
    Service for signing up a new user.

    Args:
        username: str,
        password: str

    Returns:
        user object if signup successful.
        False if signup not succesfull.
    """    
    #"""Service for signing up a new user"""
    response = store_user(username, password)
    # To do: Move prints to text_ui?
    if response:
        print(f"{bcolors.OKCYAN}--------------------")
        print(f"{username} created")
        print(f"--------------------{bcolors.ENDC}")
        return login(username, password)
    return False
