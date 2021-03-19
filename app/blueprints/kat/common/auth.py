from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash

from flask import current_app as a

auth = HTTPBasicAuth()



@auth.verify_password
def verify_password(username, password):
    with a.app_context():  
        if username in a.config['AUTH_USERS'] and check_password_hash(a.config['AUTH_USERS'].get(username), password):
            return username
        return None


@auth.error_handler
def unauthorized():
    return {"message": "Unauthorized access"}, 403
