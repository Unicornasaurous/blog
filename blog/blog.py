from flask import Blueprint, flash, g, redirect, render_template, request, session, url_for
from .db import get_db
bp = Blueprint("blog", __name__, url_prefix="/blog")

@bp.route("/", methods=["POST", "GET"])
def index():
    db = get_db()

    topics = db.execute("SELECT * FROM topic").fetchall()

    return render_template('blog/index.html', topics = topics)

@bp.route("/createtopic", methods=["POST", "GET"])
def createTopic():
    db = get_db()
    if request.method == "POST":
        topic = request.form['topic']
        
        db.execute("INSERT INTO topic (title) VALUES (?)", (topic,))
        db.commit()

        return redirect(url_for('blog.index'))
    
    return render_template('blog/createtopic.html')

@bp.route("/topic/<topic_title>")
def topic(topic_title):
    db = get_db()

    posts = ""
    return render_template('blog/topic.html', topic_title=topic_title)