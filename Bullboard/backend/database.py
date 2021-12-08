import bcrypt
import pymongo
import datetime
from pymongo import MongoClient
import functions

# TODO: Change from localhost to mongo when using docker, use localhost when running locally
mongoString = "mongodb://mongo:27017"

def connect():
    client = MongoClient(mongoString)
    return client.bullboard

#for direct messages, make emails and username unique
def verify_unused_email(user_info):
    db = connect()
    found_user = db.users.find_one({'Email': user_info['email']})
    if found_user:
        return False
    else:
        return True

def verify_login(user_info):
    db = connect()
    found_user = db.users.find_one({'Email': user_info['email']})
    # User Exists
    if found_user:
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
        'UBIT': functions.html_escaper(user_info['email']).split('@')[0],
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

def email_retrieve_user(email):
    db = connect()
    result = db.users.find_one({"Email": email})
    return result

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
            'UB Athlete': data['traits']['athlete'],
            'Scholar': data['traits']['scholar'],
            'Early Riser': data['traits']['earlyRiser'],
            'Pride': data['traits']['pride'],
            'Foodie': data['traits']['foodie'],
            'Pet Owner': data['traits']['petOwner'],
            'Car Owner': data['traits']['carOwner'],
            'Gamer': data['traits']['gamer'],
            'Gym Rat': data['traits']['workout'],
            'Night Owl': data['traits']['nightOwl']
        }
    json = {
        'Budget': data['budget'],
        'Major': functions.html_escaper(data['major']),
        'Standing': functions.html_escaper(data['standing']),
        'Housing Status': functions.html_escaper(data['status']),
        'Traits': traits
    }
    if image_name != '':
        json['Picture'] = image_name
    return json


def add_post(user, post):
    db = connect()
    json = {
        'First Name': user['First Name'],
        'Last Name': user['Last Name'],
        'Post': functions.html_escaper(post['post']),
        'Posted': datetime.datetime.now(),
    }
    db.posts.insert_one(json)
    get_posts()

def get_posts():
    db = connect()
    result = db.posts.find().sort('Posted', pymongo.DESCENDING)
    return result

def fetch_logged():
    db = connect()
    online = []
    collection = db.users.find({})
    for doc in collection:
        if len(doc["Token"]) != 0:
            online.append(doc)
    return online



def add_message(sender, data):
    db = connect()
    receiver = db.users.find_one({"UBIT": data['Recipient']})
    if receiver:
        json = {
            'Sender_to_Recipient': sender['First Name'] + " " + sender['Last Name'] + " to " + receiver['First Name'] + " " + receiver['Last Name'],
            'Sender': sender['UBIT'],
            'Recipient': receiver['UBIT'],
            'Message': functions.html_escaper(data['Message']),
            'Sent': datetime.datetime.now(),
        }
        db.messages.insert_one(json)
        get_messages(sender, receiver)


def get_messages(sender, receiver):
    db = connect()
    sender_receiver = sender['First Name'] + " " + sender['Last Name'] + " to " + receiver['First Name'] + " " + receiver['Last Name']
    result = db.messages.find({"Sender_to_Recipient": sender_receiver}).sort('Sent', pymongo.DESCENDING)
    return result

#def get_receiver(sender):
    #db = connect()
    #ubit = sender["UBIT"]
    #messages = db.messages.find_one({"Sender": ubit})
    #if messages:
        #receiver = db.users.find_one({messages['Recipient']})
        #if receiver:
            #return receiver

