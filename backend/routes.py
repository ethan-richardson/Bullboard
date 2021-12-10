import actions

# Dictionary holding all possible GET requests
get_routes = {
    "/login": actions.login,
    "/": actions.login,
    "/register": actions.register,
    "/functions.js": actions.resp_to_html_paths,
    "/canvas.js": actions.resp_to_html_paths,
    "/styles.css": actions.resp_to_html_paths,
    "/newsfeed": actions.newsfeed,
    "/profile": actions.profile,
    "/edit": actions.edit,
    "/map": actions.map,
    "/messages": actions.messages_home,
    "/logout": actions.logout
}

# Dictionary holding all possible POST requests
post_routes = {
    "/login_attempt": actions.login_attempt,
    "/create_account": actions.create_account,
    "/add_post": actions.add_post,
    "/edit_profile": actions.edit_profile,
    "/send_message": actions.send_message,
}