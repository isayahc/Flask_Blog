from flask import Blueprint, render_template

from flaskr.model import Post

main = Blueprint("main",__name__)


@main.route('/')
def index():
    posts = Post.query.all()
    return render_template('home.jinja', posts=posts)

@main.route('/about')
def about():
    return render_template('about.jinja')
