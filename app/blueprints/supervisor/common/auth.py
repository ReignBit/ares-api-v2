from flask_httpauth import HTTPBasicAuth
from werkzeug.security import check_password_hash

from app.__main__ import a


auth = HTTPBasicAuth()
users = a.config['AUTH_USERS']


@auth.verify_password
def verify_password(username, password):
    if username in users and check_password_hash(users.get(username), password):
        return username
    return None


@auth.error_handler
def unauthorized():
    return {"message": "Unauthorized access"}, 403
