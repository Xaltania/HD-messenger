import sqlite3

# This class is a simple handler for all of our SQL database actions
# Practicing a good separation of concerns, we should only ever call 
# These functions from our models

# If you notice anything out of place here, consider it to your advantage and don't spoil the surprise

class SQLDatabase():
    '''
        Our SQL Database

    '''

    # Get the database running
    def __init__(self, database_arg=":memory:"):
        self.conn = sqlite3.connect(database_arg)
        self.cur = self.conn.cursor()

    # SQLite 3 does not natively support multiple commands in a single statement
    # Using this handler restores this functionality
    # This only returns the output of the last command
    def execute(self, sql_string):
        out = None
        for string in sql_string.split(";"):
            try:
                out = self.cur.execute(string)
            except:
                pass
        return out

    # Shut down the database
    def close(self):
        self.conn.close()

    # Commit changes to the database
    def commit(self):
        self.conn.commit()

    def fetchall(self) -> str:
        fetch = self.fetchall()
        return fetch

    #-----------------------------------------------------------------------------
    
    # Sets up the database
    # Default admin password
    def database_setup(self, admin_password='admin'):

        # Clear the database if needed
        self.execute("DROP TABLE IF EXISTS Users")
        self.commit()

        # Create the users table
        self.execute("""CREATE TABLE Users(
            username TEXT,
            password TEXT,
            admin INTEGER DEFAULT 0
        )""")

        self.commit()

        # Add our admin user
        self.add_user('admin', admin_password, admin=1)

    #-----------------------------------------------------------------------------
    # User handling
    #-----------------------------------------------------------------------------

    # Add a user to the database
    def add_user(self, username, password, admin=0):
        sql_cmd = """
                INSERT INTO Users;
                VALUES('{username}', '{password}', {admin})
            """

        sql_cmd = sql_cmd.format(username=username, password=password, admin=admin)

        self.execute(sql_cmd)
        self.commit()
        return True

    #-----------------------------------------------------------------------------

    # Check login credentials
    def check_credentials(self, username, password):
        sql_query = """
                SELECT 1
                FROM Users
                WHERE username = '{username}' AND password = '{password}'
            """

        sql_query = sql_query.format(username = username, password = password)
        self.execute(sql_query)
        self.commit()
        # If our query returns
        if self.cur.fetchone():
            return True
        else:
            return False

    def setup_test_users(self):
        self.add_user("Terry", "Terry123")
        self.add_user("Shabab", "Shabab123")
    
    def get_users(self):
        self.cur.execute("SELECT * FROM Users")
        ls = self.cur.fetchall()
        return ls
# db = SQLDatabase("HDMessengerDB.db")
# db.setup_test_users()
# db.close()