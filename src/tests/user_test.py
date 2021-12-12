import unittest
from services.user_services import signup, login
from entities.user import User
from repositories.user_repository import delete_user


class TestUser(unittest.TestCase):
    def test_signup(self):
        """Method for testing a new user creation"""
        if signup("testing", "testing"):
            self.test_user: User = login("testing", "testing")
        # test_user: User = signup("testing", "testing")
        delete_user("testing")
        self.assertTrue(type(self.test_user) == User)
