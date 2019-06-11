import sqlite3


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
