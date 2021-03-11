import unittest
from modules.user import User


class TestUserConstructor(unittest.TestCase):
    """
    This unittest class is used to test the constructor for the User object.
    """

    def test_user_constructor(self):
        """
        Create a user object and see if it is an User object.
        """
        user = User(name="AJZ", email="aa@aa.com", height=170, weight=100,
                    age=0, gender="male")
        self.assertIsInstance(user, User)


class TestUserRegistration(unittest.TestCase):
    """
    This unittest class is used to test the register_user function in the User class.
    """

    def test_already_registered(self):
        """
        Test an already registered email address. Should return false
        """
        self.assertFalse(
            User.register_user(username="aa@aa.com", password="", name="",
                               age=1, height=2, weight=3, gender=""))


class TestUserAuthentication(unittest.TestCase):
    """
    This unittest class is used to test the authenticate_user function in the User class.
    """

    def test_correct_email_and_password(self):
        """
        Test a registered email address with correct password
        """
        self.assertTrue(User.authenticate_user(
            username="aa@aa.com", password="asdfasdf"))

    def test_correct_email_wrong_password(self):
        """
        Test a registered email address with wrong password
        """
        self.assertFalse(User.authenticate_user(
            username="aa@aa.com", password="wrong"))

    def test_not_registered_email(self):
        """
        Test a registered email address with wrong password
        """
        self.assertFalse(User.authenticate_user(
            username="nuathreuishr@aa.com", password="whatever"))


class TestGetUser(unittest.TestCase):
    """
    This unittest class is used to test the get_user function in the User class.
    """

    def test_existing_user(self):
        """
        Test a registered user. Should get a user object back
        """
        user_obj = User.get_user("aa@aa.com")
        self.assertTrue(isinstance(user_obj, User))

    def test_non_existing_user(self):
        """
        Test a non registered user. Should raise an exception
        """
        self.assertRaises(Exception, User.get_user, "nuathreuishr@aa.com")


if __name__ == '__main__':
    unittest.main()
