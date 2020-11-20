from logging import error
from os import environ
from functools import wraps
from six.moves.urllib.parse import urlencode
from werkzeug.exceptions import HTTPException
import json
import sys


from flask import (
    current_app as app, 
    redirect, 
    render_template, 
    session,
    url_for,
    jsonify,
    Flask,
    flash,
    Blueprint
)

from flask_login import (
    current_user,
    login_required,
    login_user,
    logout_user
)


from flaskr import db

from flaskr.auth import auth0, requires_auth
from flaskr.model import User

from flaskr.blueprints.post.forms import PostForm


users = Blueprint('users', __name__,static_url_path='users')


@users.route('/callback')
def callback_handling():
    # Handles response from token endpoint
    auth0.authorize_access_token()
    resp = auth0.get('userinfo')
    userinfo = resp.json()

    user_source = userinfo['sub'].split('|')[0] # store this is database
    #possiblity for crash 
    # probably add to session

    # Store the user information in flask session.
    session['jwt_payload'] = userinfo
    session['profile'] = {
        'user_id': userinfo['sub'],
        'name': userinfo['name'].title(),
        'picture': userinfo['picture'],
        'user_source':user_source.lower(),
        'email':userinfo['email'].lower()
    }

    existing_user = User.query.filter(
            User.email == userinfo['email'].lower()
        ).first()
    
    if existing_user and existing_user.user_source.lower() != user_source.lower():
        # need to use a flash message
        print(f"Please use {existing_user.user_source} to login")
        return redirect('/')
    elif existing_user:
        # make sure login is properly set up 
        login_user(existing_user)
        return redirect('/')
    else:
        new_user = User( 
            name=userinfo['name'].title(),
            email=userinfo['email'].lower(),
            profile_pic=userinfo['picture'],
            user_source=user_source.lower()
        ) # make sure all of the data is lower
        
        db.session.add(new_user)  # Adds new User record to database
        db.session.commit()
        login_user(new_user, force=True)
        return redirect('/')


@users.route('/login')
def login():
    return auth0.authorize_redirect(redirect_uri=f'{environ.get("FLASK_BASE_URL")}/callback')

@users.route('/dashboard')
@requires_auth
def dashboard():
    return render_template('dashboard.html',
                           userinfo=session['profile'],
                           userinfo_pretty=json.dumps(session['jwt_payload'], indent=4))

@users.route('/logout')
def logout():
    # Clear session stored data
    session.clear()
    # Redirect user to logout endpoint
    params = {'returnTo': url_for('main.index', _external=True), 'client_id': environ.get("AUTH0_CLIENT_ID")}
    return redirect(auth0.api_base_url + '/v2/logout?' + urlencode(params))

@users.route("/testing")
def about():
    return "hello"