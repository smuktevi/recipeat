import pandas as pd
# from constants import *
from .constants import *
import json
from pyrebase import pyrebase
# from bag_of_ingredients import BagOfIngredients
from .bag_of_ingredients import BagOfIngredients

firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
db = firebase.database()  # Get a reference to the database service


class User:

    def __init__(self, name="", email="", height=0, weight=0, age=0, gender=""):
        self.name = name
        self.email = email
        self.height = height
        self.weight = weight
        self.age = age
        self.gender = gender
        self.bag_of_ingredients = BagOfIngredients(email)

    @staticmethod
    def get_user(username):
        # TODO Read from firebase realtime database. Build user object and return it.
        conn = get_postgresql_connection()
        cur = conn.cursor()
        command = "select * from Users where user_id = '{}'".format(username)
        # command = "select * from Users"
        cur.execute(command)
        row = cur.fetchone()
        cur.close()
        conn.close()

        new_user = User(name=row[1], email=row[0], height=row[3], weight=row[4], age=row[5], gender=row[6])
        return new_user

    @staticmethod
    def authenticate_user(username, password):
        try:
            auth.sign_in_with_email_and_password(username, password)  # Log the user in
        except:
            return False
        return True

    @staticmethod
    def register_user(username, password, name, age, height, weight, gender):
        try:
            # Successful Registration
            # Writes new user to postgreSQL
            conn = get_postgresql_connection()
            cur = conn.cursor()
            command = "INSERT INTO Users VALUES('{}','{}','{}',{},{},{},'{}')".format(username, name, username, height,
                                                                                      weight, age, gender)
            cur.execute(command)
            cur.close()
            conn.close()

            auth.create_user_with_email_and_password(username, password)

            return True
        except:
            return False




