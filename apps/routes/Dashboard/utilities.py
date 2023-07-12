from flask_jwt_extended import decode_token
from ... import app

def decode_jwt(token):
    try:
        decoded_token = decode_token(token, app.config['SECRET_KEY'])
        return decoded_token
    except Exception:
        return None


def get_templates():
    pass

def get_count_invitation():
    pass

def get_count_guest():
    pass

def get_count_greeting():
    pass