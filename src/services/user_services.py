from repositories.user_repository import verify_user
from repositories.user_repository import store_user


'''Service for logging in a user'''
def login(username, password):
    response=verify_user(username, password)
    #To do: Move prints to text_ui?
    if response:
        print(username, "logged in")
        print("-----------")
        return username
    else:
        print("----------")
        print("User not found or incorrect password")
        print("----------")
        return None


def logout():
    #To be done
    pass


'''Service for signing up a new user '''
def signup(username, password):
    response=store_user(username, password)
    #To do: Move prints to text_ui?
    if response:
        print("----------")
        print(username, "created")
        return verify_user (username, password)
    else:
        return False

