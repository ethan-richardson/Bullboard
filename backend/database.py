import bcrypt
from pymongo import MongoClient

# TODO: Change from localhost to mongo
mongoString = "mongodb://localhost:27017"

def connect():
    client = MongoClient(mongoString)
    return client.bullboard

def verify_login(user_info):
    db = connect()
    user_info = db.users.find_one({'Email': user_info['email']})
    # User Exists
    if user_info:
        # Password matches
        if bcrypt.checkpw(user_info['Password'], data['password']):
            return True
        # Invalid password
        else:
            return False
    # User does not exist
    else:
        return False


