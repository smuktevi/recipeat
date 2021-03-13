import psycopg2
from .constants import *
from urllib.parse import parse_qsl, urljoin, urlparse

###########################################################################
# The Database class is a high-level wrapper around the psycopg2
#    library. It allows users to create a postgresql database connection and
#    write to or fetch data from the selected database.
###########################################################################


class Database:
    """
    The constructor of the Database class

    The constructor can either be passed the name of the database to open
    or not, it is optional. The database can also be opened manually with
    the open() method or as a context manager.

    param
    url - [Optional] the url of the database to open.

    see: open()
    """

    def __init__(self, url=None):

        self.conn = None  # database psycopg connector to postgres defined.
        self.cursor = None  # cursor to database table defined.

        if url:
            self.open(url)  # url used to open if passed during instantiation.

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()

    def open(self, url=None):
        """
        Opens a new database connection. This function manually opens a new database connection. The database
        can also be opened in the constructor or as a context manager.

        param: self

        return: boolean,
            True - if open connection successful.
            False - if open connection fails.
        """

        try:
            if url:
                self.url = urlparse(url)
            else:
                self.url = urlparse(
                    db_url
                )  # Access credentials via the passed on url. The url must
                # be parsed with the urlparse library.
            self.conn = psycopg2.connect(
                database=self.url.path[1:],
                user=self.url.username,
                password=self.url.password,
                host=self.url.hostname,
                port=self.url.port,
            )
            self.conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
            self.cursor = self.conn.cursor()
        except:
            print("Log: Error has occurred while opening database!")
            return False
        return True

    def close(self):
        """
        Function to close a datbase connection.
        The database connection needs to be closed before you exit a program,
        otherwise changes might be lost. You can also manage the database
        connection as a context manager, then the closing is done for you. If
        you opened the database connection with the open() method or with the
        constructor, you must close the connection with this
        method.

        param: self

        return: Boolean
        """

        if self.conn:  # Execute set of closing statements for database connection.
            self.conn.commit()
            self.cursor.close()
            self.conn.close()
            return True
        return False

    def get(self, table, columns="*", limit=None, where=None):
        """
        Function to fetch/query data from a database.
        This is the main function used to query a database for data.

        params:
            table - The name of the database's table to query from.
            columns - The string of columns, comma-separated, to fetch.
            limit - Optionally, a limit of items to fetch.

        return:
            list(table records) - if query successful
            False - if query fails
        """

        if where:  # check if the query has a where clause
            query = "SELECT {0} from {1} WHERE {2};".format(columns, table, where)
        else:
            query = "SELECT {0} from {1};".format(columns, table)
        try:
            self.cursor.execute(query)
            rows = self.cursor.fetchall()  # fetch data
        except:
            print("Log: Could not fetch rows!")
            return False
        return rows[len(rows) - limit if limit else 0 :]

    def write(self, table, columns, data):
        """
        Function to write data to the database.
        The write() function inserts new data into a table of the database.

        params:
            table - The name of the database's table to write to.
            columns - The columns to insert into, as a comma-separated string.
            data - The new data to insert, as a comma-separated string.

        return: Boolean
        """

        query = "INSERT INTO {0} ({1}) VALUES ({2});".format(table, columns, data)
        try:
            self.cursor.execute(query)
        except:
            print("Log: Error in Inserting!")
            return False
        return True

    def query(self, sql):
        """
        Function to query any other SQL statement.
        This function is there in case you want to execute any other sql
        statement other than a write or get.

        params:
            sql - A valid SQL statement in string format.
        """
        try:
            self.cursor.execute(sql)
            if ("DELETE" in sql) or ("UPDATE" in sql):
                if self.cursor.rowcount == 0:
                    return False
        except:
            print("Log: Error in query execution!")
            return False
        return True
