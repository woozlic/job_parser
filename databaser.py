import psycopg2
from secret_codes import DB_USER, DB_PASSWORD, DB_NAME, DB_HOST, PORT
from psycopg2 import errorcodes


def create_table_subscribed():

    conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST)

    cursor = conn.cursor()
    cursor.execute("""CREATE TABLE users_subscribed
                        (
                            Id INT PRIMARY KEY NOT NULL,
                            User_Id CHAR(30) UNIQUE NOT NULL,
                            Status CHAR(30)
                        );""")
    conn.close()
    return True


def create_table_links():
    """
    Creates table for links
    :return: True if table was created, False if table already exists
    """
    conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST, port=PORT)
    cursor = conn.cursor()
    try:
        cursor.execute("""CREATE TABLE links2
                        (
                          Id INT PRIMARY KEY NOT NULL, 
                          link CHAR(50) UNIQUE
                        );""")
        conn.commit()
        return True
    except Exception as err:
        print(f'Ошибка psycopg2: {errorcodes.lookup(err.pgcode)}')
        return False
    finally:
        conn.close()


def add_link(link: str) -> bool:
    """
    Returns True if link didn't exist in DB and append to it
    Returns False if link already exist in DB
    :param link: link
    :return: True or False
    """

    result = False

    conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST, port=PORT)
    cursor = conn.cursor()
    cursor.execute('SELECT link FROM links WHERE link = %s', (link, ))
    row = cursor.fetchone()
    if row is None:
        cursor.execute('INSERT INTO links(link) VALUES (%s)', (link, ))
        conn.commit()
        conn.close()
        result = True
    return result


def subscribe(user_id):

    conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST, port=PORT)
    cursor = conn.cursor()
    cursor.execute('')
    conn.close()

