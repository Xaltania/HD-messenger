# USYD CODE CITATION ACKNOWLEDGEMENT
# I declare that the following code template is distributed by Winston Wijaya
# With changes made to implement security features

from flask import Flask, render_template, request, abort, url_for, redirect, session
from flask_socketio import SocketIO
from flask_admin import Admin, AdminIndexView
from flask_admin.contrib.sqla import ModelView

from models import User

import db
import secrets
import bcrypt
# import logging

# this turns off Flask Logging, uncomment this to turn off Logging
# log = logging.getLogger('werkzeug')
# log.setLevel(logging.ERROR)


app = Flask(__name__,static_folder='static')

# secret key used to sign the session cookie
app.config['SECRET_KEY'] = secrets.token_hex()
# Database path
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///database/main.db"

# Flask-admin setup
admin = Admin(app, index_view=AdminIndexView(name='Admin'))
# Admin page

class UserView(ModelView):
    column_list = ('username', 'password')
    column_sortable_list = ('username',)



# Admin panel
admin.add_view(UserView(User, db.Session()))

# Custom AdminIndexView to handle the login page
class MyAdminIndexView(AdminIndexView):

    # Login page for admin
    @app.route('/admin/login', methods=['GET', 'POST'])
    def admin_login():
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']

            user = db.get_user(username)

            if user is None:
                return "Error: User does not exist!"

            pw_bytes = password.encode('utf-8')
            hash_match = bcrypt.checkpw(pw_bytes, user.password)

            if not hash_match:
                return "Error: Password does not match!"

            session['username'] = user.username

            return redirect('/admin')

        return render_template('login.jinja')

admin.index_view = MyAdminIndexView()

socketio = SocketIO(app)

# don't remove this!!
import socket_routes

@app.context_processor
def inject_user():
    if 'username' in session:
        username = session['username']
        current_user = db.get_user(username)
    else:
        current_user = None
    return dict(current_user=current_user)
# index page
@app.route("/")
def index():
    return render_template("index.jinja")

# login page
@app.route("/login")
def login():    
    return render_template("login.jinja")

# handles a post request when the user clicks the log in button
@app.route("/login/user", methods=["POST"])
def login_user():
    if not request.is_json:
        abort(404)

    username = request.json.get("username")
    password = request.json.get("password")

    user =  db.get_user(username)

    if user is None:
        return "Error: User does not exist!"

    pw_bytes = password.encode('utf-8')
    hash_match = bcrypt.checkpw(pw_bytes, user.password)
    
    if not hash_match:
        return "Error: Password does not match!"
    
    # Store the username in the session
    session['username'] = user.username
    
    return url_for('home', username=request.json.get("username"))


# Logout route
@app.route("/logout", methods=["POST"])
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))

# handles a get request to the signup page
@app.route("/signup")
def signup():
    return render_template("signup.jinja")

# handles a post request when the user clicks the signup button
@app.route("/signup/user", methods=["POST"])
def signup_user():
    if not request.is_json:
        abort(404)
    username = request.json.get("username")
    password = request.json.get("password")

    pw_bytes = password.encode('utf-8')
    pw_hash = bcrypt.hashpw(pw_bytes, bcrypt.gensalt())

    if db.get_user(username) is None:
        db.insert_user(username, pw_hash)
        return url_for('home', username=username)
    # Store the username in the session
    user =  db.get_user(username)
    session['username'] = user.username
    return "Error: User already exists!"



# Route to display the forum page
@app.route("/forum")
def forum():
    # Retrieve existing forum posts from the database
    posts = db.get_posts()

    return render_template("forum.jinja", posts=posts)

# Route to handle form submission and create a new post
@app.route("/forum/create_post", methods=["POST"])
def create_post():
    content = request.form.get("content")
    anonymous = bool(request.form.get("anonymous"))
    author = session['username']

    # Save the post to the database
    db.create_post(content, anonymous, author)

    return redirect(url_for("forum"))

# handler when a "404" error happens
@app.errorhandler(404)
def page_not_found(_):
    return render_template('404.jinja'), 404

# home page, where the messaging app is
@app.route("/home")
def home():
    
    if request.args.get("username") is None:
        abort(404)
        # request.args.get("username")
    # username = session['username']
    username = request.args.get("username")
    return render_template("home.jinja", username=username)



if __name__ == '__main__':
    ssl_context = ('certificate/localhost.crt', 'certificate/localhost.key')
    socketio.run(app=app, ssl_context=ssl_context, port=443, debug = True)
