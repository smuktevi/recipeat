import unittest
from modules.database import Database
from unittest.mock import Mock


class TestDatabaseConnection(unittest.TestCase):
    """
    This Class is used to test the connection to a database.
    """
    def __init__(self, *args, **kwargs):
        super(TestDatabaseConnection, self).__init__(*args, **kwargs)
        self.good_url = "postgres://fbporsgtkyccmc:846ffc72335cec44f0861518fc4d1acfda4f890f52471fdb31dda4a637f3932a@ec2-100-24-139-146.compute-1.amazonaws.com:5432/d9umass2brvfdv"
        
    def test_open_database_success(self):
        """
        Test if database connection successful. Should return true.
        """
        self.assertTrue(Database(self.good_url))

    def test_open_database_failure(self):
        """
        Test if database connection successful. Should return true.
        """
        bad_url = "bad_url.com"
        self.assertFalse(Database().open(bad_url))

    def test_close_database(self):
        """
        Test if database closes successfully.
        """
        db = Database(self.good_url)
        self.assertTrue(db.close())


class TestDatabaseInsertQuery(unittest.TestCase):
    """ 
    This Class is used to test the insert query on the database.
    """
    def __init__(self, *args, **kwargs):
        super(TestDatabaseInsertQuery, self).__init__(*args, **kwargs)
        self.good_url, self.db = None, None
        self.generate_stubs()

    def generate_stubs(self):
        self.good_url = "postgres://fbporsgtkyccmc:846ffc72335cec44f0861518fc4d1acfda4f890f52471fdb31dda4a637f3932a@ec2-100-24-139-146.compute-1.amazonaws.com:5432/d9umass2brvfdv"
        self.db = Database(self.good_url)

    def test_insert_query_tables(self):
        """
        Test if insert query works for both Tables.
        """
        self.assertTrue(self.db.write(table="users", columns="user_id, name, email, height, weight, age, gender, diet, intolerances", data="'temp_test@gmail.com', 'temp', 'q@gmail.com', 999, 999, 12, 'temp', 'temp', 'temp'"))
        self.assertTrue(self.db.write(table="bagofingredients", columns="user_id, ingredient, ingredient_name, amount, unit", data="'temp_test@gmail.com', '12 grams sugar', 'sugar', '12', 'grams'"))


class TestDatabaseSelectQuery(unittest.TestCase):
    """
    This Class is used to test the select query on the database.
    """
    def __init__(self, *args, **kwargs):
        super(TestDatabaseSelectQuery, self).__init__(*args, **kwargs)
        self.good_url, self.db = None, None
        self.generate_stubs()
        
    def generate_stubs(self):
        self.good_url = "postgres://fbporsgtkyccmc:846ffc72335cec44f0861518fc4d1acfda4f890f52471fdb31dda4a637f3932a@ec2-100-24-139-146.compute-1.amazonaws.com:5432/d9umass2brvfdv"
        self.db = Database(self.good_url)

    def test_select_query_bagofingredients(self):
        """
        Test if select query works for Bag of Ingredients Table.   
        """
        self.assertTrue(self.db.get(table="bagofingredients", columns="*"))
        self.assertTrue(self.db.get(table="bagofingredients", columns="*",
                               where="user_id='q@gmail.com'"))   # test where clause

    def test_select_query_users(self):
        """
        Test if select query works for Users Table.
        """
        self.assertTrue(self.db.get(table="users", columns="*"))
        self.assertTrue(self.db.get(table="users", columns="*",
                               where="user_id='q@gmail.com'"))   # test where clause
    
class TestDatabaseDeleteQuery(unittest.TestCase):
    """ 
    This Class is used to test DELETE from the database.
    """
    def __init__(self, *args, **kwargs):
        super(TestDatabaseDeleteQuery, self).__init__(*args, **kwargs)
        self.good_url, self.db = None, None
        self.generate_stubs()

    def generate_stubs(self):
        self.good_url = "postgres://fbporsgtkyccmc:846ffc72335cec44f0861518fc4d1acfda4f890f52471fdb31dda4a637f3932a@ec2-100-24-139-146.compute-1.amazonaws.com:5432/d9umass2brvfdv"
        self.db = Database(self.good_url)

    def test_delete_query_tables(self):
        """
        Test if DELETE works for both Tables.
        """
        self.assertTrue(self.db.query("DELETE FROM users WHERE user_id='temp_test@gmail.com'"))
        self.assertTrue(self.db.query("DELETE FROM bagofingredients WHERE user_id='temp_test@gmail.com'"))
