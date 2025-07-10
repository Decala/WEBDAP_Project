from flask import *
import webbrowser
import threading
from shelf_storage import *
from services import *
app = Flask(__name__)


@app.route('/success', methods=['POST', 'GET'])
def success():
    expected_inputs = ["nm", "pw"]
    user_input = [request.form.get(name) if request.method == 'POST' else request.args.get(name)
                  for name in expected_inputs]

    identifier = new_account_by_class(user_input[0], user_input[1], 1, [])
    return redirect(url_for("successful", identifier=identifier))


@app.route('/successful/<identifier>')
def successful(identifier):
    user_info = account_info_by_class(identifier)
    return render_template(r"successful.html", name=user_info[0], account_no=identifier, password=user_info[1])


@app.route('/register')
def register():
    return render_template(r"register.html")


@app.route('/')
def home():
    Services("Login", url_for("login"))
    Services("register", url_for("register"))
    template = render_template(r"main.html", available_services=Services.all_services)
    clear_service()
    return template


@app.route("/login")
def login():
    return "Login is true"


@app.route("/sign_up")
def signup():
    return "signup"


def open_browser():
    webbrowser.open_new("http://127.0.0.1:5000/")


if __name__ == '__main__':
    threading.Timer(2.0, open_browser).start()
    # Webpage will open twice if debug = True.

    app.run(debug=True)





