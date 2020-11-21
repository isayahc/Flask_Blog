from flask import Blueprint, render_template, request

from flaskr.model import Post, User

main = Blueprint("main",__name__)


@main.route('/')
def index():
    page = request.args.get('page',1, type=int)
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
    return render_template('home.jinja', posts=posts)

@main.route('/about')
def about():
    return render_template('about.jinja')

@main.route('/user/<string:username>')
def user_post(username):
    page = request.args.get('page',1, type=int)
    user = User.query.filter_by(name=username).first_or_404()
    posts = Post.query.filter_by(author=user)\
        .order_by(Post.date_posted.desc())\
        .paginate(page=page, per_page=5)
    return render_template('user_post.jinja', posts=posts, user=user)
