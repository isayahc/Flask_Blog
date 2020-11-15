from os import environ
from functools import wraps

from . import oauth

#register auth0
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

