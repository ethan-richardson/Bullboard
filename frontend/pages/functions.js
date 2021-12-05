const socket = new WebSocket('ws://' + window.location.host + '/websocket');

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
    }
    return JSON.stringify(jsonMap);
}

function loginJSON() {
    var email = document.getElementById("email");
    var password = document.getElementById("password");
    var jsonMap = {
        email: email.value,
        password: password.value
    }
    return JSON.stringify(jsonMap);
}