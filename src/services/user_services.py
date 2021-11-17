from repositories.users import login
from repositories.users import signup


def login_service(username, password):
    response=login(username, password)
    if response:
        print(username, "logged in")
        print("user_id", response)
        return username
    else:
        print("User not found or incorrect password")
        return None

def logout():
    #to be done
    pass


def signup_service(username, password):
    response=signup(username, password)
    if response:
        print(username, "created")
        login_service (username, password)
    else:
        print ("signup failed")

