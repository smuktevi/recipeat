import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

if __name__ == '__main__':
    conn = psycopg2.connect(dbname="d9umass2brvfdv", user="fbporsgtkyccmc",
                            password="846ffc72335cec44f0861518fc4d1acfda4f890f52471fdb31dda4a637f3932a",
                            host="ec2-100-24-139-146.compute-1.amazonaws.com", sslmode='require')
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cur = conn.cursor()

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
        ingredient VARCHAR NOT NULL,
        ingredient_name VARCHAR,
        amount INTEGER,
        unit VARCHAR,
        PRIMARY KEY (user_id, ingredient_name),
        FOREIGN KEY (user_id)
            REFERENCES Users (user_id)
            ON UPDATE CASCADE ON DELETE CASCADE
        )
        """
    )

    # create table one by one
    for command in commands:
        cur.execute(command)

    # close communication with the PostgreSQL database server
    cur.close()
    conn.close()
