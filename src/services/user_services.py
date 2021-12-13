from repositories.user_repository import verify_user, store_user
from services.portfolio_services import get_portfolios
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
    if response:
        user = User(response[0], response[1], response[2])
        portfolios = get_portfolios(user)
        user.portfolios = portfolios
        return user
    return False


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
    response = store_user(username, password)
    if response:
        return True
    return False
