from flask import *
import webbrowser
import threading
from shelf_storage import *
from services import *
app = Flask(__name__)


@app.route('/success', methods=['POST', 'GET'])
def success():
    # Captures user input, Creates a new user account, then redirects into successful page
    expected_inputs = ["nm", "pw"]
    user_input = [request.form.get(name) if request.method == 'POST' else request.args.get(name)
                  for name in expected_inputs]

    identifier = new_account_by_class(user_input[0], user_input[1], 1, [])
    return redirect(url_for("successful", identifier=identifier))


@app.route('/successful/<identifier>')
def successful(identifier):
    # Upon successful account creation.

    user_info = account_info_by_class(identifier)
    return render_template(r"successful.html",
                           name=user_info[0],
                           account_no=identifier,
                           password=user_info[1],
                           home_page=url_for("home"))


@app.route('/register')
def register():
    return render_template(r"register.html")


@app.route('/')
def home():
    if Config.identifier:
        services_logged_in()
        username = account_info(Config.identifier).username
        username = ", " + username + "!"
    else:
        services_logged_out()
        username = "! Please Select A Service:"
    template = render_template(r"main.html", available_services=Services.all_services, username=username)
    clear_service()
    return template


@app.route("/login")
def login():
    return render_template("login.html")


@app.route("/login_attempt", methods=['POST', 'GET'])
def login_attempt():
    expected_inputs = ["id", "pw"]
    user_input = [request.form.get(name) if request.method == 'POST' else request.args.get(name)
                  for name in expected_inputs]
    try:
        account = static_db()["Account"][user_input[0]]
    except KeyError:
        return redirect(url_for("login"))
    else:
        if account.password == user_input[1]:
            return redirect(url_for("on_login", identifier=user_input[0]))
        else:
            return redirect(url_for("login"))


@app.route("/sign_up")
def signup():
    return "signup"


@app.route("/logout")
def logout():
    Config.identifier = False
    return redirect(url_for("home"))


@app.route("/logging_in/<identifier>")
def on_login(identifier):
    Config.identifier = identifier
    return redirect(url_for("home"))


def open_browser():
    webbrowser.open_new("http://127.0.0.1:5000/")
    services_logged_out()


def services_logged_out():
    Services("Login", url_for("login"))
    Services("register", url_for("register"))


def services_logged_in():
    Services("Logout", url_for("logout"))


if __name__ == '__main__':
    threading.Timer(3.0, open_browser).start()
    # Webpage will open twice if debug = True.

    app.run(debug=True)

