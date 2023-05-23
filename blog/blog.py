from flask import Blueprint, flash, g, redirect, render_template, request, session, url_for

bp = Blueprint("blog", __name__, url_prefix="/blog")

@bp.route("/", methods=["POST", "GET"])
def index():
    return render_template('blog/index.html')