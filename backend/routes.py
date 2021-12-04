import actions

# Dictionary holding all possible GET requests
get_routes = {
    "/login":actions.login,
    "/": actions.login,
    "/register": actions.register,
    "/functions.js":actions.resp_to_html_paths,
    "/styles.css":actions.resp_to_html_paths,
    "/Bull_Board_Mat.png":actions.resp_to_html_paths,
    "/bull_knocker.jpeg": actions.resp_to_html_paths,
    "/welcome_mat.png": actions.resp_to_html_paths,
}

# Dictionary holding all possible POST requests
post_routes = {

}