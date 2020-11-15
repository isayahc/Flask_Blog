from os import environ
from functools import wraps
from six.moves.urllib.parse import urlencode
from werkzeug.exceptions import HTTPException
import json

from flask import (
    current_app as app, 
    redirect, 
    render_template, 
    session,
    url_for,
    jsonify,
    Flask
)

from flask_login import (
    current_user,
    login_required,
    login_user,
    logout_user
)

from . import oauth
from . import db
from .model import User

# print(User.query.all())

auth0 = oauth.register(
    'auth0',
    client_id=environ.get("AUTH0_CLIENT_ID"),
    client_secret=environ.get("AUTH0_CLIENT_SECRET"),
    api_base_url=environ.get("AUTH0_BASE_URL"),
    access_token_url=f'{environ.get("AUTH0_BASE_URL")}/oauth/token',
    authorize_url=f'{environ.get("AUTH0_BASE_URL")}/authorize',
    client_kwargs={
        'scope': 'openid profile email',
    },
)

# Here we're using the /callback route.
@app.route('/callback')
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
        'user_source':user_source,
        'email':userinfo['email'].lower()
    }

    existing_user = User.query.filter(
            User.email == userinfo['email']
        ).first()

    if not existing_user:
        #uniform set-up
        new_user = User(
            name=userinfo['name'].title(),
            email=userinfo['email'].title(),
            profile_pic=userinfo['picture'],
            user_source=user_source.title()
        )
        
        db.session.add(new_user)  # Adds new User record to database
        db.session.commit()
        login_user(new_user)
        return redirect('/dashboard')
    
    elif existing_user and existing_user.user_source != user_source and existing_user:
        return redirect('/')
    
    else:
        login_user(existing_user)
        return redirect('/dashboard')

    


    # if existing_user and existing_user.user_source != user_source:
    #     return redirect('/')
    # if  existing_user and existing_user.email == userinfo['email']:
    #     return redirect('/')
    # elif existing_user:
    #     login_user(existing_user)
    #     return redirect('/dashboard')
    # else:
    #     new_user = User(
    #         name=userinfo['name'],
    #         email=userinfo['email'],
    #         profile_pic=userinfo['picture'],
    #         user_source=user_source
    #     )
        
    #     db.session.add(new_user)  # Adds new User record to database
    #     db.session.commit()
    #     login_user(new_user)



    # add condition to prevent user from using different sources
    # if email match but source does not
    #   return error telling user to use their original source
    # if user_email is not in db 
    #   add new User to db
    # use SQL_TUTORIAL TO FIGURE IT OUT

    # return redirect('/dashboard')

@app.route('/login')
def login():
    return auth0.authorize_redirect(redirect_uri=f'{environ.get("FLASK_BASE_URL")}/callback')

def requires_auth(f):
  @wraps(f)
  def decorated(*args, **kwargs):
    if 'profile' not in session:
      # Redirect to Login page here
      return redirect('/')
    return f(*args, **kwargs)

  return decorated

@app.route('/dashboard')
@requires_auth
def dashboard():
    return render_template('dashboard.html',
                           userinfo=session['profile'],
                           userinfo_pretty=json.dumps(session['jwt_payload'], indent=4))

@app.route('/logout')
def logout():
    # Clear session stored data
    session.clear()
    # Redirect user to logout endpoint
    params = {'returnTo': url_for('index', _external=True), 'client_id': environ.get("AUTH0_CLIENT_ID")}
    return redirect(auth0.api_base_url + '/v2/logout?' + urlencode(params))

@app.route('/')
def index():
    # add template rendering 
    return render_template('home.jinja')
