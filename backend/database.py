import bcrypt
from pymongo import MongoClient
import functions

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
    hashed_pw = functions.hash_password(user_info['password'])
    traits = {
            'UB Athlete': False,
            'Scholar': False,
            'Early Riser': False,
            'Pride': False,
            'Foodie': False,
            'Pet Owner': False,
            'Car Owner': False,
            'Gamer': False,
            'Gym Rat': False,
            'Night Owl': False
        }
    db.users.insert_one({'Email': user_info['email'], 'First Name': user_info['first'], 'Last Name': user_info['last'],
                         'Picture': '', 'Token': '', 'Password': hashed_pw, 'Birthday': user_info['birthday'], 'Major':
                         '', 'Standing': user_info['standing'], 'Traits': traits, 'Budget': '', 'Housing Status': '',
                         'Hometown': ''})
    return


def store_token(email, token):
    db = connect()
    hashed_token = functions.hash_token(token)
    db.users.update_one({"Email": email}, {"$set": {"Token": hashed_token}})
    return


def retrieve_user(token):
    db = connect()
    #Hash users current token
    token = functions.hash_token(token)
    result = db.users.find_one({"Token": token})
    return result

# def add_post():