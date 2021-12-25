import unittest
from initiate_db import initialize_database
initialize_database()
from services.user_services import signup, login
from entities.user import User
from repositories.user_repository import delete_user


class TestUser(unittest.TestCase):
    def setUp(self):
        initialize_database()
        
    def test_signup(self):
        """Method for testing a new user creation"""
        if signup("testing", "testing"):
            self.test_user: User = login("testing", "testing")
        delete_user("testing")
        self.assertTrue(type(self.test_user) == User)

    def test_login_with_wrong_password(self):
        """Method for testing a new user creation"""
        if signup("testing", "testing"):
            self.test_user: User = login("testing", "wrong-password")
        delete_user("testing")
        self.assertTrue(type(self.test_user) != User)
