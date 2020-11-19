from flask import Blueprint, render_template

main = Blueprint("main",__name__)

posts = [
    {
        'author': 'Corey Schafer',
        'title': 'Blog Post 1',
        'content': 'First post content',
        'date_posted': 'April 20, 2018'
    },
    {
        'author': 'Jane Doe',
        'title': 'Blog Post 2',
        'content': 'Second post content',
        'date_posted': 'April 21, 2018'
    }
]

@main.route('/blog')
def post():
    return render_template('post.jinja', posts=posts)

@main.route('/about')
def about():
    return render_template('about.jinja')

@main.route('/')
def index():
    # add template rendering
    return render_template('home.jinja')
