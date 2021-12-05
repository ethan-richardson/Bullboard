import actions

# Dictionary holding all possible GET requests
get_routes = {
    "/login": actions.login,
    "/": actions.login,
    "/register": actions.register,
    "/functions.js": actions.resp_to_html_paths,
    "/styles.css": actions.resp_to_html_paths,
    "/newsfeed": actions.newsfeed,
    "/profile": actions.profile,
}

# Dictionary holding all possible POST requests
post_routes = {
    "/login_attempt": actions.login_attempt,
    "/create_account": actions.create_account,
    "/add_post": actions.add_post,
    "/update_account": actions.update_account
}