from .constants import *
from pyrebase import pyrebase
from .bag_of_ingredients import BagOfIngredients

firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
db = firebase.database()  # Get a reference to the database service


class User:
    """
    User class. Creates an User object. The user object has name, email,
    height, weight, and age as attributes. The class has methods to return
    the user object from the database, authenticate an existing user,
    and registering a new user.
    """

    def __init__(self, name="", email="", height=0, weight=0, age=0,
                 gender=""):
        """
        Constructor to initialize the User object.

        :param name: String. Name of the User.
        :param email: String. Email of the User.
        :param height: int. Height of the User.
        :param weight: int. Weight of the User.
        :param age: int. Age of the User
        :param gender: String. Gender of the User
        """
        self.name = name
        self.email = email
        self.height = height
        self.weight = weight
        self.age = age
        self.gender = gender
        self.bag_of_ingredients = BagOfIngredients(email)

    @staticmethod
    def get_user(username):
        """
        Static function used to query from postgreSQL with given username
        and return a constructed User object.

        :param username: String. Username (email) of the User.
        :return: User. Returns the constructed User object from the query.
        """
        conn = get_postgresql_connection()
        cur = conn.cursor()
        command = "select * from Users where user_id = '{}'".format(username)
        cur.execute(command)
        row = cur.fetchone()
        cur.close()
        conn.close()

        # Check if user exists. If not raise Exception.
        if row is None:
            raise Exception("User is not registered")
        new_user = User(name=row[1], email=row[0], height=row[3],
                        weight=row[4], age=row[5], gender=row[6])
        return new_user

    @staticmethod
    def authenticate_user(username, password):
        """
        Static function that checks if user credentials are correct to
        login. Returns true if the credentials are correct and false
        otherwise.

        :param username: String. Username (email) of the User.
        :param password: String. Password of the User.
        :return: Boolean. Returns true if the credentials are correct and false
        otherwise.
        """
        try:
            auth.sign_in_with_email_and_password(
                username, password)
        except:
            return False
        return True

    @staticmethod
    def register_user(username, password, name, age, height, weight, gender):
        """
        Static method used to register a new user into the database. Returns
        true if the new user was successfully created, false otherwise.

        :param username: String. Username (email) of the User.
        :param password: String. Password of the User.
        :param name: String. Name of the User.
        :param age: int. Age of the User
        :param height: int. Height of the User.
        :param weight: int. Weight of the User.
        :param gender: String. Gender of the User

        :return: Boolean. Returns true if the new user was successfully
        created, false otherwise.
        """
        try:
            # Successful Registration
            # Writes new user to postgreSQL
            conn = get_postgresql_connection()
            cur = conn.cursor()
            command = "INSERT INTO Users VALUES('{}', '{}', '{}', {}, {}, " \
                      "{}, '{}')".format(
                username, name, username, height,
                weight, age, gender)
            cur.execute(command)
            cur.close()
            conn.close()
            
            auth.create_user_with_email_and_password(username, password)

            return True
        except:
            return False

    @staticmethod
    def delete_user(username, password):
        """
        Static method to delete a user. Requires username and password to
        confirm delete.

        :param username: String. Username (email) of the User.
        :param password: String. Password of the User.
        :return: Boolean. True if successfully deleted, false otherwise.
        """
        try:
            user = auth.sign_in_with_email_and_password(username, password)
            auth.delete_user_account(id_token=user['idToken'])

            conn = get_postgresql_connection()
            cur = conn.cursor()
            command = "DELETE FROM Users where user_id = '{}'".format(username)
            cur.execute(command)
            cur.close()
            conn.close()
            return True
        except:
            return False
