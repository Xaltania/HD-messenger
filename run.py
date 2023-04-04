'''
    This is a file that configures how your server runs
    You may eventually wish to have your own explicit config file
    that this reads from.

    For now this should be sufficient.

    Keep it clean and keep it simple, you're going to have
    Up to 5 people running around breaking this constantly
    If it's all in one file, then things are going to be hard to fix

    If in doubt, `import this`
'''

#-----------------------------------------------------------------------------
import os
import sys
from bottle import run

#-----------------------------------------------------------------------------
# You may eventually wish to put these in their own directories and then load 
# Each file separately

# For the template, we will keep them together

import model
import view
import controller
import sql

#-----------------------------------------------------------------------------

# It might be a good idea to move the following settings to a config file and then load them
# Change this to your IP address or 0.0.0.0 when actually hosting
host = 'localhost'

# Test port, change to the appropriate port to host
port = 8081

# Turn this off for production
debug = True

def run_server():    
    '''
        run_server
        Runs a bottle server
    '''
    run(host=host, port=port, debug=debug)

#-----------------------------------------------------------------------------
# Optional SQL support
# Comment out the current manage_db function, and 
# uncomment the following one to load an SQLite3 database

"""
def manage_db():
    '''
        Blank function for database support, use as needed
    '''
    pass
"""

    
def manage_db():
    '''
        manage_db
        Starts up and re-initialises an SQL databse for the server
    '''
    database_args = "HDMessengerDB.db" # Currently runs in RAM, might want to change this to a file if you use it
    sql_db = sql.SQLDatabase(database_arg=database_args)
    print("".center(80, '-'))
    print("Database Manager".center(80, '-'))
    print("".center(80, '-'))
    print("Type '/help' for commands")
    while True:
        usr_in = input("Enter command: ")
        
        match usr_in:
            case "/help":
                print("""
                Input may be directly SQL to modify database
                List of commands:
                /db_setup - create a table for users
                /users_clear - completely clear database of all users and messages
                /quit - exit the manager
                /setup_test_users - add the test users into the database
                /users_show - display a list of all users
                """)
            case "/db_setup":
                sql_db.database_setup()
                print("Setting up...")
                print("Set-up successful")
            case "/users_show":
                print(sql_db.get_users())
            case "/setup_test_users":
                print("Setting up test users...")
                sql_db.setup_test_users()
                print("Set-up successful")
            case "/users_clear":
                confirm = input("WARNING: You are about to clear all users and passwords. Are you sure? (Y/n)")
                while confirm != "Y" and confirm != "n":
                    confirm = input("Please select from: 'Y' for yes, 'n' for no.")
                if confirm == "Y":
                    sql_db.execute("DELETE FROM Users")
                    sql_db.commit()
                    print("Users cleared")
                elif confirm == "n":
                    pass
            case "/quit":
                print("Exiting...")
                break
            case _:
                print(f"SQL: {usr_in}")
                msg = sql_db.execute(usr_in)
                sql_db.commit()
                if msg != None:
                    print(msg)
                    print(sql_db.fetchall())
                
    
    # while True:


#-----------------------------------------------------------------------------

# What commands can be run with this python file
# Add your own here as you see fit

command_list = {
    'manage_db' : manage_db,
    'server'       : run_server
}

# The default command if none other is given
default_command = 'server'

def run_commands(args):
    '''
        run_commands
        Parses arguments as commands and runs them if they match the command list

        :: args :: Command line arguments passed to this function
    '''
    commands = args[1:]

    # Default command
    if len(commands) == 0:
        commands = [default_command]

    for command in commands:
        if command in command_list:
            command_list[command]()
        else:
            print("Command '{command}' not found".format(command=command))

#-----------------------------------------------------------------------------

run_commands(sys.argv)