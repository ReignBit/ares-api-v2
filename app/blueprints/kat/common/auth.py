from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash


auth = HTTPBasicAuth()
users = {"kat": generate_password_hash("test")}


@auth.verify_password
def verify_password(username, password):
    if username in users and check_password_hash(users.get(username), password):
        return username
    return None


@auth.error_handler
def unauthorized():
    return {"message": "Unauthorized access"}, 403
