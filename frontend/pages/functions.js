//const socket = new WebSocket('ws://' + window.location.host + '/websocket');

//Generates registration json string
function registrationJSON() {
    var email = document.getElementById("email");
    var password = document.getElementById("password");
    var password2 = document.getElementById("rePassword");
    var firstName = document.getElementById("firstName");
    var lastName = document.getElementById("lastName");
    var birthday = document.getElementById("birthday");
    var standing = document.getElementById("standing");
    if (password.value !== password2.value) {
        document.getElementById("invalid").innerHTML = "Passwords must match"
        return "";
    }
    var jsonMap = {
        email: email.value,
        password: password.value,
        rePassword: password2.value,
        first: firstName.value,
        last: lastName.value,
        birthday: birthday.value,
        standing: standing.value
    };
    return JSON.stringify(jsonMap);
}

//Sends registration info to server
function processRegistration() {
    const json = registrationJSON();
    if(json !== "") {
        const request = new XMLHttpRequest();
        request.onreadystatechange = function () {
            var feedback = document.getElementById("invalid");
            if (this.readyState === 4 && this.status === 201) {
                window.location.replace('/');
            }  else if (this.readyState === 4 && this.status === 404) {
                if (this.responseText.startsWith("Password")) {
                    feedback.innerHTML = "Password does not meet all requirements";
                } else if (this.responseText.startsWith("Email")) {
                    feedback.innerHTML = "Email is not valid or a duplicate account exists";
                }
            }
        };
        request.open("POST", "/create_account");
        request.send(json);
    }
}

//Generates login json string
function loginJSON() {
    var email = document.getElementById("email");
    var password = document.getElementById("password");
    var jsonMap = {
        email: email.value,
        password: password.value
    };
    return JSON.stringify(jsonMap);
}

//Sends login info to server
function processLogin() {
    const json = loginJSON();
    if (json !== "") {
        const request = new XMLHttpRequest();
        const feedback = document.getElementById("invalid");
        request.onreadystatechange = function () {
            if (this.readyState === 4 && this.status === 200) {
                window.location.replace('/newsfeed')
            } else if (this.readyState === 4 && this.status === 404) {
                feedback.innerHTML = "Invalid Login";
            }
        };
        request.open("POST", "/login_attempt");
        request.send(json);
    }
}

//Generates update profile json string
async function updateJSON() {
    var budget = document.getElementById("budget");
    var standing = document.getElementById("standing");
    var status = document.getElementById("status");
    var major = document.getElementById("major");
    var profPic = document.getElementById("profilePicture");
    var hometown = document.getElementById("hometown");
    var selectedTraits = getTraits();
    budget = (parseInt(budget.value));
    var jsonMap = {
        budget: budget,
        major: major.value,
        status: status.value,
        standing: standing.value,
        hometown: hometown.value,
        traits: selectedTraits,
    };
    if(profPic.files.length > 0) {
        await getBase64(profPic.files[0]).then(
            function(result) {
                jsonMap["picture"] = {name: profPic.files[0].name, image: result};
            });
    }
    else {
        jsonMap["picture"] = {name: "", image: ""};
    }
    return JSON.stringify(jsonMap);
}

function getTraits() {
    var traitIDs = ['athlete', 'scholar', 'nightOwl', 'earlyRiser', 'gamer', 'carOwner', 'petOwner', 'pride', 'foodie',
    'workout']
    var traitOutput = {}
    for(var i = 0; i < traitIDs.length; i++) {
        var currentTrait = traitIDs[i]
        traitOutput[currentTrait] = document.getElementById(currentTrait).checked;
    }
    return traitOutput;
}


function getBase64(file) {
  return new Promise((resolve, reject) => {
    const reader = new FileReader();
    reader.readAsDataURL(file);
    reader.onload = () => resolve(reader.result);
    reader.onerror = error => reject(error);
  });
}

//Sends user profile changes to server
async function processUpdate() {
    const json = await updateJSON();
    if (json !== "") {
        const request = new XMLHttpRequest();
        request.onreadystatechange = function () {
            if (this.readyState === 4 && this.status === 200) {
                window.location.assign('/profile')
            } else if (this.readyState === 4 && this.status === 404) {
                alert('changes could not be made')
            }
        };
        request.open("POST", "/edit_profile");
        request.send(json);
    }
}

//Generates post adding json string
function addPostJSON() {
    var post = document.getElementById("post");
    return JSON.stringify({'post': post.innerHTML});
}

//Sends post info to server
function processPost() {
    const json = addPostJSON();
    console.log(json)
    if (json !== "") {
        const request = new XMLHttpRequest();
        request.onreadystatechange = function () {
            if (this.readyState === 4 && this.status === 201) {
                window.location.replace('/newsfeed');
            } else if (this.readyState === 4 && this.status === 404) {
                alert("Could not add post")
            }
        };
        request.open("POST", "/add_post");
        request.send(json);
    }
}


//Generates post adding json string
function sendMessageJSON() {
    const post = document.getElementById("message");
    const recipient = document.getElementById("recipient");
    const message = post.innerHTML;
    post.innerHTML = "";
    return JSON.stringify({'Message': message, 'Recipient': recipient.innerHTML});
}


function processMessage() {
    const json = sendMessageJSON();
    console.log(json)
    if (json !== "") {
        const request = new XMLHttpRequest();
        request.onreadystatechange = function () {
            if (this.readyState === 4 && this.status === 201) {
                // window.location.replace('/newsfeed');
            } else if (this.readyState === 4 && this.status === 404) {
                alert("Could not add post")
            }
        };
        request.open("POST", "/send_message");
        request.send(json);
    }
}