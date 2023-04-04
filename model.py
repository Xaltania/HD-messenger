'''
    Our Model class
    This should control the actual "logic" of your website
    And nicely abstracts away the program logic from your page loading
    It should exist as a separate layer to any database or data structure that you might be using
    Nothing here should be stateful, if it's stateful let the database handle it
'''
import view
import random
from sql import SQLDatabase

# Initialise our views, all arguments are defaults for the template
page_view = view.View()

#-----------------------------------------------------------------------------
# Index
#-----------------------------------------------------------------------------

def index():
    '''
        index
        Returns the view for the index
    '''
    return page_view("index")

#-----------------------------------------------------------------------------
# Login
#-----------------------------------------------------------------------------

def login_form():
    '''
        login_form
        Returns the view for the login_form
    '''
    return page_view("login")

#-----------------------------------------------------------------------------
# Sign up
#-----------------------------------------------------------------------------

def signup_form():
    '''
        signup_form
        Returns the view for the signup_form
    '''
    return page_view("/signup/signup")

#-----------------------------------------------------------------------------

# Check signup details
def signup_check(username, password, confirm_pwd):
    '''
        signup_check
        Checks that username is unique and that passwords match

        :: username :: The username
        :: password :: The password
        :: confirm_pwd :: Re-entered password

        Returns a successful signup or failure
    '''
    # Open database
    sql_db = db_open()

    exists = sql_db.user_exists(username=username)
    if exists or password != confirm_pwd:
        pass
        page_view("signup_name_fail")
    else:
        pass
        # Load to success!
    

# Check the login credentials
def login_check(username, password):
    '''
        login_check
        Checks usernames and passwords

        Salting and hashing performed here

        :: username :: The username
        :: password :: The password

        Returns either a view for valid credentials, or a view for invalid credentials
    '''
    # Open database 
    sql_db = db_open()
    # By default assume good creds

    login = True
    valid = sql_db.check_credentials(username=username, password=password)
    print(f"password is {valid}")
    
    if not valid:
        err_str = "The username or password entered was invalid."
        login = False
    
    sql_db.close()
    if login: 
        return page_view("valid", name=username)
    else:
        return page_view("invalid", reason=err_str)

#-----------------------------------------------------------------------------
# About
#-----------------------------------------------------------------------------

def about():
    '''
        about
        Returns the view for the about page
    '''
    return page_view("about", garble=about_garble())



# Returns a random string each time
def about_garble():
    '''
        about_garble
        Returns one of several strings for the about page
    '''
    garble = ["leverage agile frameworks to provide a robust synopsis for high level overviews.", 
    "iterate approaches to corporate strategy and foster collaborative thinking to further the overall value proposition.",
    "organically grow the holistic world view of disruptive innovation via workplace change management and empowerment.",
    "bring to the table win-win survival strategies to ensure proactive and progressive competitive domination.",
    "ensure the end of the day advancement, a new normal that has evolved from epistemic management approaches and is on the runway towards a streamlined cloud solution.",
    "provide user generated content in real-time will have multiple touchpoints for offshoring."]
    return garble[random.randint(0, len(garble) - 1)]

#-----------------------------------------------------------------------------
# Debug
#-----------------------------------------------------------------------------

def db_open():
    '''
        Opens the database
        :return: sqlite database object
    '''
    database_args = "HDMessengerDB.db"
    sql_db = SQLDatabase(database_arg=database_args)

    return sql_db

#-----------------------------------------------------------------------------
# Debug
#-----------------------------------------------------------------------------

def debug(cmd):
    try:
        return str(eval(cmd))
    except:
        pass


#-----------------------------------------------------------------------------
# 404
# Custom 404 error page
#-----------------------------------------------------------------------------

def handle_errors(error):
    error_type = error.status_line
    error_msg = error.body
    return page_view("error", error_type=error_type, error_msg=error_msg)