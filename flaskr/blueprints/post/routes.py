from flask.globals import request
from flask.helpers import url_for
from werkzeug.exceptions import abort
from werkzeug.utils import redirect
from flaskr import db

from flask import Blueprint, render_template, flash

from flaskr.blueprints.post.forms import PostForm
from flaskr.model import Post

from flaskr.auth import auth0, requires_auth

from flask_login import current_user

post = Blueprint('post', __name__)

@post.route('/post/new', methods=['GET', 'POST'])
@requires_auth
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, content=form.content.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your post has been created!', 'success')
        return redirect(url_for('main.index'))
    return render_template('create_post.jinja', title='New Post', 
    form=form, legend='New Post')

@post.route('/post/<int:post_id>')
def single_post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post.jinja', title=post.title, post=post)

@requires_auth
@post.route('/post/<int:post_id>/update', methods=['GET', 'POST'])
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash('Your post has been updated!', 'success')
        return redirect(url_for('post.single_post',post_id=post.id_))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
    return render_template('create_post.jinja', title='Update Post', 
    form=form, legend='Update Post')


@requires_auth
@post.route('/post/<int:post_id>/delete', methods=['GET', 'POST'])
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('main.index'))
