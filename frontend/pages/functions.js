const socket = new WebSocket('ws://' + window.location.host + '/websocket');

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
                alert("Account Successfully Created!")
            }  else if (this.readyState === 4 && this.status === 404) {
                feedback.innerHTML = "Password does not meet all requirements";
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
function updateJSON() {
    var budget = document.getElementById("budget");
    var standing = document.getElementById("standing");
    var status = document.getElementById("status");
    var major = document.getElementById("major");
    var jsonMap = {
        budget: budget.value,
        major: major.value,
        status: status.value,
        standing: standing.value
    };
    return JSON.stringify(jsonMap);
}

//Sends user profile changes to server
function processUpdate() {
    const json = updateJSON();
    if (json !== "") {
        const request = new XMLHttpRequest();
        request.onreadystatechange = function () {
            if (this.readyState === 4 && this.status === 200) {
                window.location.replace('/profile')
            } else if (this.readyState === 4 && this.status === 404) {
                feedback.innerHTML = "Invalid Login";
            }
        };
        request.open("POST", "/update_account");
        request.send(json);
    }
}

//Generates post adding json string
function addPostJSON() {
    var post = document.getElementById("post");
    return JSON.stringify({'post': post});
}

//Sends post info to server
function processPost() {
    const json = addPostJSON();
    if (json !== "") {
        const request = new XMLHttpRequest();
        request.onreadystatechange = function () {
            if (this.readyState === 4 && this.status === 201) {
                const post = document.createElement("p");
                post.innerHTML = json['post']
                post.className = 'post'
            } else if (this.readyState === 4 && this.status === 404) {
                alert("Could not add post")
            }
        };
        request.open("POST", "/add_post");
        request.send(json);
    }
}