from flask import Blueprint, flash, g, redirect, render_template, request, session, url_for
from .db import get_db
bp = Blueprint("blog", __name__, url_prefix="/blog")

@bp.route("/", methods=["POST", "GET"])
def index():
    return render_template('blog/index.html')

@bp.route("/createtopic", methods=["POST", "GET"])
def createTopic():
    return render_template('blog/createtopic.html')