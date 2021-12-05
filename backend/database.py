import bcrypt
from pymongo import MongoClient
import hashlib

# TODO: Change from localhost to mongo
mongoString = "mongodb://localhost:27017"

def connect():
    client = MongoClient(mongoString)
    return client.bullboard

def verify_login(user_info):
    db = connect()
    found_user = db.users.find_one({'Email': user_info['email']})
    # User Exists
    if user_info:
        # Password matches
        if bcrypt.checkpw(user_info['password'].encode(), found_user['Password'].encode()):
            return True
        # Invalid password
        else:
            return False
    # User does not exist
    else:
        return False

def add_user(user_info):
    db = connect()
    hashedPW = hash_password(user_info['password'])
    db.users.insert_one({'Email': user_info['email'], 'First Name': user_info['first'], 'Last Name': user_info['last'],
                         'Token': '', 'Password': hashedPW, 'Birthday': user_info['birthday'], 'Major': '',
                         'Standing': user_info['standing'], 'Traits': {}, 'Budget': '', 'Housing Status': '',
                         'Hometown': ''})
    return

def hash_password(password):
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode("utf-8")

def store_token(email, token):
    db = connect()
    hashedToken = hash_token(token)
    db.users.update_one({"Email": email}, {"$set": {"Token": hashedToken}})
    return

def hash_token(token):
    return hashlib.sha256(token.encode()).hexdigest()
