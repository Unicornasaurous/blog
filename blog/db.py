import sqlite3

import click
from flask import current_app, g


def get_db():
    """
    Creates a connection to the database for the unique request and 
    returns that connection

    'g' is an object that stores data for each unique request to the flask instance
    """
    if 'db' not in g:
        #creates connection to the database at the path found for key 'DATABASE' in the app config
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row
    return g.db

def close_db(e=None):
    """
    Pops the db out of the g object and closes it if it exists
    """
    db = g.pop('db', None)

    if db is not None:
        db.close()

def init_db():
    """
    Initializes the database based on 'schema.sql' 
    """
    db = get_db()

    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))

@click.command('admin')
@click.option('--user', help="The user desired to be admin")
def make_admin(user):
    """
    Function is a callback for CLI command. Function marks the admin column
    for a specified user as '1' to indicate that that user is an admin
    """
    db = get_db()
    #get user row
    u = db.execute("SELECT * FROM user WHERE username = ?", (user,)).fetchone()
    #check if user exists
    if u is not None:
        db.execute("UPDATE user SET admin = 1 WHERE username = ?", (user,))
        db.commit()
        click.echo(f"{user} has been made an admin")
    else:
        click.echo(f"{user} doesn't exist!")


@click.command('init-db')
def init_db_command():
    """
    Command line function for initializing the db
    """
    click.echo("You are about to initialize the database. Any data will be wiped. Proceed? y/n")
    answer = input().lower()

    if answer == 'y':
        init_db()
        click.echo("Initialized database")
    else:
        click.echo("Database init canceled")

def init_app(app):
    """
    Function for registering close_db and init_db_command for the app instance
    """

    #Registers close_db as the function to run when a request has ended
    app.teardown_appcontext(close_db)
    #Registers init_db_command as a flask command
    app.cli.add_command(init_db_command)
    #Register admin command as a flask command 
    app.cli.add_command(make_admin)