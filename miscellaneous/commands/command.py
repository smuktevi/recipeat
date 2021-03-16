import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

if __name__ == '__main__':
    """
    This module was used to create tables for the postgreSQL. Was only run
    once.
    """

    conn = psycopg2.connect(dbname="d9umass2brvfdv", user="fbporsgtkyccmc",
                            password=("846ffc72335cec44f0861518fc4d1acfda4f890"
                                      "f52471fdb31dda4a637f3932a"),
                            host="ec2-100-24-139-146.compute-1.amazonaws.com",
                            sslmode='require')
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cur = conn.cursor()

    commands = "ALTER TABLE BagOfIngredients ALTER COLUMN amount TYPE INTEGER;"
    cur.execute(commands)

    # close communication with the PostgreSQL database server
    cur.close()
    conn.close()
