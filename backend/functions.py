import base64
import hashlib
import bcrypt
import re
import secrets
import database
import file
import time
from datetime import date
from base64 import b64decode

# Verifies password requirements are satisfied
def verify_password(password, password2):
    if password != password2:
        return False
    if re.match(r"^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{8,}$", password):
        return True
    else:
        return False


# Generates login cookie
def login_token():
    return secrets.token_hex(16)


# Hashes login cookie token to be stored in database
def hash_token(token):
    return hashlib.sha256(token.encode()).hexdigest()


# Hashes password with bcrypt
def hash_password(password):
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode("utf-8")


# Escapes html to prevent injection
def html_escaper(text):
    text = text.replace('&', '&amp;')
    text = text.replace('<', '&lt;')
    text = text.replace('>', '&gt;')
    return text


# Loads user profile
def load_profile(token):
    user = database.retrieve_user(token)
    if user:
        body = file.read_file("../frontend/pages/profile.html")
        body = body.replace(b'{{First Name}}', user['First Name'].encode())
        body = body.replace(b'{{Last Name}}', user['Last Name'].encode())
        body = body.replace(b'{{Standing}}', user['Standing'].encode())
        body = body.replace(b'{{Age}}', age(user['Birthday']).encode())
        body = body.replace(b'{{Status}}', user['Housing Status'].encode())
        body = body.replace(b'{{Major}}', user['Major'].encode())
        body = body.replace(b'{{Hometown}}', user['Hometown'].encode())
        body = body.replace(b'{{Budget}}', str(user['Budget']).encode())
        if user['Picture'] == '':
            body = body.replace(b'{{Prof Pic}}', b'/images/prof_pics/default.png')
        else:
            body = body.replace(b'{{Prof Pic}}', b'/images/prof_pics/' + user['Picture'].encode())
        body = body.replace(b'{{Traits}}', create_trait_image_tags(user['Traits']))
        return body
    else:
        return false

#Creates image tags for profile loading
def create_trait_image_tags(traits):
    output = ""
    for trait in traits:
        if traits[trait]:
            output += ("<img class=\"icon\" src=\"images/" + get_trait_image(trait) + "\" alt=\"" + trait +
                       "\" title=\"" + trait + "\"\n>")
    return output.encode()

#Gets image path
def get_trait_image(trait):
    if trait == 'UB Athlete':
        return 'athleteIcon.png'
    elif trait == 'Scholar':
        return 'scholarIcon.png'
    elif trait == 'Early Riser':
        return 'earlyRiserIcon.png'
    elif trait == 'Pride':
        return 'prideIcon.png'
    elif trait == 'Foodie':
        return 'foodieIcon.png'
    elif trait == 'Pet Owner':
        return 'petOwnerIcon.png'
    elif trait == 'Car Owner':
        return 'carOwnerIcon.png'
    elif trait == 'Gamer':
        return 'gamerIcon.png'
    elif trait == 'Gym Rat':
        return 'workoutIcon.png'
    elif trait == 'Night Owl':
        return 'nightOwlIcon.png'

#Calculates users age from birthday
def age(birthday):
    birthdate = birthday.split("-")
    today = date.today()
    age = today.year - int(birthdate[0]) - ((today.month, today.day) < (int(birthdate[1]), int(birthdate[2])))
    return str(age)

#Adds profile picture to server storage
def add_image(picture):
    if picture['name'] != '':
        name_split = picture['name'].split('.')
        #Generates unique file name
        file_name = name_split[0] + str(round(time.time() * 100000)) + '.' + name_split[1]
        image_info = picture['image']
        comma_split = image_info.split(",", 1)
        encoded_string = comma_split[1]
        image_bytes = b64decode(encoded_string)
        f = open("../frontend/pages/images/prof_pics/" + file_name, "wb")
        f.write(image_bytes)
        f.close()
        return file_name
    else:
        return ''

#Creates post elements for newsfeed template
def create_post_elements():
    output = ""
    posts = database.get_posts()
    for post in posts:
        output += ('<p class=\"newsfeedPost\"><b>' + post['First Name'] + ' ' + post['Last Name'] + '</b>: ' +
                   post['Post'] + '</p>\n')
    return output

def get_user(token):
    if token:
        user = database.retrieve_user(token)
        if user:
            return user
        else:
            return False
    else:
        return False