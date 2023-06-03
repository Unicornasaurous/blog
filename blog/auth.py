import functools

from flask import Blueprint, flash, g, redirect, render_template, request, session, url_for
from werkzeug.security import check_password_hash, generate_password_hash
from .db import get_db

#blue print 
bp = Blueprint("auth", __name__, url_prefix="/blog/auth")

@bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        #Store username and password from the request form
        username = request.form['username']
        password = request.form['password']
        #Get database
        db = get_db()
        #Set default error to None type
        error = None

        if not username and not password:
            error = "Username and Password are required"
        elif not username:
            error = "Username is required"
        elif not password:
            error = "Password is required"

        if error is None:
            try:
                db.execute("INSERT INTO user (username, password, admin) VALUES (?, ?, ?)",
                (username, generate_password_hash(password), 0),)
                db.commit()
                return redirect(url_for("auth.login"))
            except db.IntegrityError:
                error=f"User '{username}' already exists"
                print("Database integrity error")
            else:
                return redirect(url_for("auth.login"))
        
        flash(error)
    
    return render_template("auth/register.html")

@bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None
        user = db.execute("SELECT * FROM user WHERE username = ?", (username,)).fetchone()

        if user is None:
            error="Invalid username"
            print("Invalid username")
        elif not check_password_hash(user['password'], password):
            error ="Invalid password"
            print("Invalid password")
        else:
            #Store our user's ID in the session, which gets sent to 
            #web browser as a cookie to be stored and sent back with each
            #subsequent request 
            session.clear()
            session['user_id'] = user['id']
            return redirect(url_for('blog.index'))


        flash(error)
    
    return render_template("auth/login.html")


@bp.before_app_request
def load_logged_in_user():
    """This will run before every request made to the app
    is handled. Here, we get our user's ID from the session, which is
    passed back to us along with te request from the web browser. 
    Note that the session is sent to the web browser and stored--then, sent
    back. We use the user ID to find our user's info in the database and
    then store that info as a dictionary inside of our 'g' object. 
    """
    user_id = session.get('user_id')
    db = get_db()

    if user_id is None:
        g.user = None
    else:
        g.user = db.execute(
            "SELECT * FROM user WHERE id = ?", (user_id,)
        ).fetchone()

@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('blog.index'))

@bp.route('/admin-message')
def admin_message():
    """
    A message displayed to the user when they have attempted to access a view 
    without administrator privileges.
    """
    return "You thought you were slick, huh? Gotta be an admin to do this."


def login_required(view):
    """
    This can be used as a decorator for views to require that the user 
    be logged in. It checks this by checking our user object stored inside of 
    our g object. If the user is not found to be logged in, it redirects to
    the login page. 
    """
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view

def admin_required(view):
    """
    Can be used as a decorator for views to require that the user be logged in 
    as an administrator in order to access the view. 
    """
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))
        elif g.user['admin'] != 1:
            return redirect(url_for('auth.admin_message'))
        return view(**kwargs)

    return wrapped_view