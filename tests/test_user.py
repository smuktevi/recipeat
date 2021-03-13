import unittest
import pytest
from modules.user import User


class TestUserConstructor(unittest.TestCase):
    """
    This unittest class is used to test the constructor for the User object.
    """

    @pytest.mark.order(16)
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

    @pytest.mark.order(17)
    def test_new_user(self):
        """
        Test a new user. Should return true
        """
        self.assertTrue(
            User.register_user(username="new_user@aa.com", password="asdfasdf",
                               name="", age=1, height=2, weight=3, gender="")
        )

    @pytest.mark.order(18)
    def test_already_registered(self):
        """
        Test an already registered email address. Should return false
        """
        self.assertFalse(
            User.register_user(username="new_user@aa.com", password="",
                               name="", age=1, height=2, weight=3, gender=""))


class TestUserAuthentication(unittest.TestCase):
    """
    This unittest class is used to test the authenticate_user function in the User class.
    """

    @pytest.mark.order(19)
    def test_correct_email_and_password(self):
        """
        Test a registered email address with correct password
        """
        self.assertTrue(User.authenticate_user(
            username="new_user@aa.com", password="asdfasdf"))

    @pytest.mark.order(20)
    def test_correct_email_wrong_password(self):
        """
        Test a registered email address with wrong password
        """
        self.assertFalse(User.authenticate_user(
            username="new_user@aa.com", password="wrong"))

    @pytest.mark.order(21)
    def test_not_registered_email(self):
        """
        Test a registered email address with wrong password
        """
        self.assertFalse(User.authenticate_user(
            username="not_registered@aa.com", password="whatever"))


class TestGetUser(unittest.TestCase):
    """
    This unittest class is used to test the get_user function in the
    User class.
    """

    @pytest.mark.order(22)
    def test_existing_user(self):
        """
        Test a registered user. Should get a user object back
        """
        user_obj = User.get_user("new_user@aa.com")
        self.assertTrue(isinstance(user_obj, User))

    @pytest.mark.order(23)
    def test_non_existing_user(self):
        """
        Test a non registered user. Should raise an exception
        """
        self.assertRaises(Exception, User.get_user, "not_registered@aa.com")


class TestDeleteUser(unittest.TestCase):
    """
    This unittest class is used to test the delete_user function in the
    User class.
    """

    @pytest.mark.order(24)
    def test_delete_user(self):
        """
        Delete an existing user. Should return true
        """
        self.assertTrue(User.delete_user("new_user@aa.com", "asdfasdf"))

    @pytest.mark.order(25)
    def test_fail_delete_user(self):
        """
        Delete an non-existing user. Should return false
        """
        self.assertFalse(User.delete_user("not_registered@aa.com", "asdfasdf"))


if __name__ == '__main__':
    unittest.main()
