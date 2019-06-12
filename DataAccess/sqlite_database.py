import sqlite3
from sqlite3 import Error


def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)

    return None


def create_table(conn, create_table_sql):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)


def create_user(conn, user):
    """
    Create a new project into the projects table
    :param conn:
    :param project:
    :return: project id
    """
    sql = "INSERT INTO users VALUES (:username, :password, :age, :country)",
#                   {'username': user.username, 'password': user.password, 'age': user.age, 'country': user.country}
    cur = conn.cursor()
    cur.execute(sql)
    return cur.lastrowid


def set_up():
    database = "C:/Users/Shai/SoftEngProjDB.db"
    sql_create_users_table = """CREATE TABLE IF NOT EXISTS users (
                     username text,
                     password text,
                     age integer,
                     country text
                     )"""
    sql_create_stores_table = """CREATE TABLE IF NOT EXISTS stores (
                 username text,
                 password text,
                 age integer,
                 country text
                 )"""
    sql_create_items_table = """CREATE TABLE IF NOT EXISTS items (
                 username text,
                 password text,
                 age integer,
                 country text
                 )"""
    sql_create_store_owners_table = """CREATE TABLE IF NOT EXISTS storeOwners (
                    username text,
                    password text,
                    age integer,
                    country text
                    )"""
    sql_create_store_managers_table = """CREATE TABLE IF NOT EXISTS storeManagers (
                    username text,
                    password text,
                    age integer,
                    country text
                    )"""

    # create a database connection
    conn = create_connection(database)
    if conn is not None:
        create_table(conn, sql_create_users_table)
        create_table(conn, sql_create_stores_table)
        create_table(conn, sql_create_items_table)
        create_table(conn, sql_create_store_owners_table)
        create_table(conn, sql_create_store_managers_table)
    else:
        print("Error! cannot create the database connection.")


if __name__ == '__main__':
    set_up()

#
# conn = sqlite3.connect('WebsiteData.db')
# c = conn.cursor()
#
# # c.execute("DROP TABLE users")
# def set_up():
#     conn.commit()
#     c.execute("""CREATE TABLE IF NOT EXISTS users (
#                         username text,
#                         password text,
#                         age integer,
#                         country text
#                         )""")
#
#     c.execute("""CREATE TABLE IF NOT EXISTS stores (
#                 username text,
#                 password text,
#                 age integer,
#                 country text
#                 )""")
#
#     c.execute("""CREATE TABLE IF NOT EXISTS items (
#                 username text,
#                 password text,
#                 age integer,
#                 country text
#                 )""")
#     # conn.commit()
#
#     c.execute("""CREATE TABLE IF NOT EXISTS storeOwners (
#                     username text,
#                     password text,
#                     age integer,
#                     country text
#                     )""")
#     # conn.commit()
#
#     c.execute("""CREATE TABLE IF NOT EXISTS storeManagers (
#                     username text,
#                     password text,
#                     age integer,
#                     country text
#                     )""")
#     # conn.commit()
#
# def add_to_users(user):
#     set_up()
#     with conn:
#         c.execute("INSERT INTO users VALUES (:username, :password, :age, :country)",
#                   {'username': user.username, 'password': user.password, 'age': user.age, 'country': user.country})
#         conn.commit()
#
#
# def get_all_users():
#     c.execute("SELECT * FROM users")
#     return c.fetchall()
#
#
# print(get_all_users())
# # conn.commit()
#
# # conn.close()
