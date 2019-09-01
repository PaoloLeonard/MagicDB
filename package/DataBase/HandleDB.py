import psycopg2 as psycopg2
from .config import config


def create_table_deck():
    """Create tables in the PostgreSQL database"""
    command = (
        """
        CREATE TABLE deck (
            deck_id SERIAL PRIMARY KEY, 
            deck_name VARCHAR(255) NOT NULL,
            deck_format VARCHAR(255) NOT NULL,
            deck_list cards [],
            UNIQUE (deck_id)
        )
        """
    )
    conn = None
    try:
        # read the connection parameters
        params = config()
        # connect to the PostgreSQL server
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        # create table one by one
        cur.execute(command)
        # close communication with the PostgreSQL database server
        cur.close()
        # commit the changes
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print("Database connection closed.")
