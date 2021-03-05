import os
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT


if __name__ == '__main__':

    '''
    postgresql_config = {
        'host': "ec2-100-24-139-146.compute-1.amazonaws.com",
        'dbname': "d9umass2brvfdv",
        'user': "fbporsgtkyccmc",
        'password': "846ffc72335cec44f0861518fc4d1acfda4f890f52471fdb31dda4a637f3932a",
        'sslmode': "require"
    }
    '''
    conn = psycopg2.connect(dbname="d9umass2brvfdv", user="fbporsgtkyccmc", password="846ffc72335cec44f0861518fc4d1acfda4f890f52471fdb31dda4a637f3932a", host="ec2-100-24-139-146.compute-1.amazonaws.com", sslmode='require')
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)

    cur = conn.cursor()

    '''
    commands = (
        """
        CREATE TABLE Users (
            user_id VARCHAR(255) PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            email VARCHAR(255) NOT NULL,
            height INTEGER,
            weight INTEGER,
            age INTEGER,
            gender VARCHAR(255)
        )
        """,
        """
        CREATE TABLE BagOfIngredients (
            user_id VARCHAR(255) NOT NULL,
            ingredient VARCHAR,
            PRIMARY KEY (user_id, ingredient),
            FOREIGN KEY (user_id)
                REFERENCES Users (user_id)
                ON UPDATE CASCADE ON DELETE CASCADE
        )
        """
    )
    '''

    #commands = ["INSERT INTO Users VALUES ('test1', 'test1', 'test1', 1, 2, 3, 'test1')"]
    commands = ["select * from BagOfIngredients;", "select * from Users;"]

    # create table one by one
    for command in commands:
        cur.execute(command)

    # For reading queries
    '''
    row = cur.fetchone()
    while row is not None:
        print(row)
        row = cur.fetchone()
    '''

    # close communication with the PostgreSQL database server
    cur.close()

    conn.close()
