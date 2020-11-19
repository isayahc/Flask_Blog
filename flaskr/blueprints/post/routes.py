from flaskr import db

from flask import Blueprint, render_template

from flaskr.blueprints.post.forms import PostForm

from flaskr.auth import auth0, requires_auth
from flaskr.auth import auth0, requires_auth

post = Blueprint('post', __name__)

@post.route('/post/new', methods=['GET', 'POST'])
@requires_auth
def new_post():
    form = PostForm()
    return render_template('create_post.html', title='New Post', form=form)