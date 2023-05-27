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
        title = request.form['title']
        desc = request.form['desc']
        db.execute("INSERT INTO topic (title, desc) VALUES (?, ?)", (title, desc))
        db.commit()

        return redirect(url_for('blog.index'))
    
    return render_template('blog/createtopic.html')

@bp.route("/<topic_title>")
def topic(topic_title):
    db = get_db()
    id = request.args.get('id')
    print(f"Topic ID: {id}")
    posts = ""
    return render_template('blog/topic.html', topic_title=topic_title)

@bp.route("/<int:id>/delete")
def delete_topic(id):
    db = get_db()

    db.execute("DELETE FROM topic WHERE id = ?", (id,))
    db.commit()

    return redirect(url_for('blog.index'))

@bp.route("/<int:id>/edit", methods=["POST", "GET"])
def edit_topic(id):
    db = get_db()
    topic = db.execute("SELECT * FROM topic WHERE id = ?", (id,)).fetchone()

    if request.method == "POST":
        title = request.form['title']
        desc = request.form['desc']

        db.execute("UPDATE topic SET (title, desc) = (?, ?)", (title, desc))
        db.commit()

        return redirect(url_for('blog.index'))

    return render_template('blog/createtopic.html', topic=topic)

    
