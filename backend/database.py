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
    json = {
        'Email': functions.html_escaper(user_info['email']),
        'First Name': functions.html_escaper(user_info['first']),
        'Last Name': functions.html_escaper(user_info['last']),
        'Picture': '',
        'Token': '',
        'Password': hashed_pw,
        'Birthday': functions.html_escaper(user_info['birthday']),
        'Major': '',
        'Standing': functions.html_escaper(user_info['standing']),
        'Traits': traits,
        'Budget': 0,
        'Housing Status': '',
        'Hometown': ''
    }
    db.users.insert_one(json)
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

def update_profile(data, image_name, token):
    update_json = construct_update_json(data, image_name)
    token = functions.hash_token(token)
    db = connect()
    db.users.update_one({'Token': token}, {'$set': update_json})


def construct_update_json(data, image_name):
    traits = {
            'UB Athlete': functions.html_escaper(data['traits']['athlete']),
            'Scholar': functions.html_escaper(data['traits']['scholar']),
            'Early Riser': functions.html_escaper(data['traits']['earlyRiser']),
            'Pride': functions.html_escaper(data['traits']['pride']),
            'Foodie': functions.html_escaper(data['traits']['foodie']),
            'Pet Owner': functions.html_escaper(data['traits']['petOwner']),
            'Car Owner': functions.html_escaper(data['traits']['carOwner']),
            'Gamer': functions.html_escaper(data['traits']['gamer']),
            'Gym Rat': functions.html_escaper(data['traits']['workout']),
            'Night Owl': functions.html_escaper(data['traits']['nightOwl'])
        }
    json = {
        'Budget': functions.html_escaper(data['budget']),
        'Major': functions.html_escaper(data['major']),
        'Standing': functions.html_escaper(data['standing']),
        'Housing Status': functions.html_escaper(data['status']),
        'Traits': traits
    }
    if image_name != '':
        json['Picture'] = image_name
    return json


# def add_post():


