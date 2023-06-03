from flask import Blueprint, flash, g, redirect, render_template, request, session, url_for
from .db import get_db
from .auth import admin_required

bp = Blueprint("blog", __name__, url_prefix="/blog")

@bp.route("/", methods=["POST", "GET"])
def index():
    """
    The index view is where all topic items populate for the user. Topics
    are fetched from the database and then passed onto jinja for templating.
    """
    db = get_db()

    topics = db.execute("SELECT * FROM topic").fetchall()

    return render_template('blog/index.html', topics = topics)

@bp.route("/createtopic", methods=["POST", "GET"])
def createTopic():
    """
    This is the view that allows users to create new topics
    """
    db = get_db()
    if request.method == "POST":
        title = request.form['title']
        desc = request.form['desc']
        db.execute("INSERT INTO topic (title, desc) VALUES (?, ?)", (title, desc))
        db.commit()

        return redirect(url_for('blog.index'))
    
    return render_template('blog/createtopic.html')

@bp.route("/<topic_title>")
def topic(topic_title):
    """
    Topic view handles requests to view specific topics. The topic ID 
    is passed as an argument in the URL and accessed via request.args
    """
    db = get_db()
    topic_id = request.args.get('id')
    
    posts = db.execute("SELECT * FROM post WHERE topic_id = ?", (topic_id,)).fetchall()
    return render_template('blog/topic.html', topic_title=topic_title, posts=posts)

@bp.route("/<int:id>/delete")
@admin_required
def delete_topic(id):
    """
    Handles requests to delete a certain topic. The topic ID is passed as a URL
    variable from the user and used to delete the desired topic. 
    """
    db = get_db()

    db.execute("DELETE FROM topic WHERE id = ?", (id,))
    db.commit()

    #TO-DO: Delete all associated posts under a topic

    return redirect(url_for('blog.index'))

@bp.route("/<int:id>/edit", methods=["POST", "GET"])
@admin_required
def edit_topic(id):
    """View handles requests to edit topic. It allows users to 
    change the values associated with a topic, such as title and description"""
    db = get_db()
    topic = db.execute("SELECT * FROM topic WHERE id = ?", (id,)).fetchone()

    if request.method == "POST":
        title = request.form['title']
        desc = request.form['desc']

        db.execute("UPDATE topic SET (title, desc) = (?, ?)", (title, desc))
        db.commit()

        return redirect(url_for('blog.index'))

    return render_template('blog/createtopic.html', topic=topic)

@bp.route("/<topic_title>/<post_title>")
def post():
    """Post view handles requests for a specific post. Post ID
    is passed as a URL arg and accessed using request.args"""
    db = get_db()
    post_id = request.args['id']

    post = db.execute("SELECT * FROM post WHERE id = ?", (id,)).fetchone()

    return render_template('blog/post.html', post=post)

@bp.route("/<topic_title>/createpost")
def create_post(topic_title):
    """View handles requests to create a new post under the desired
    topic.
    """
    db = get_db()
    if request.method == "POST":
        title = request.form['title']
        body = request.form['body']
        db.execute("INSERT INTO topic (title, desc) VALUES (?, ?)", (title, body))
        db.commit()

        return redirect(url_for('blog.index'))
    
    return render_template('blog/createpost.html')