from flask import *
import webbrowser
from shelf_storage import *
app = Flask(__name__)


@app.route('/success/<identifier>')
def success(identifier):
    user_info = account_info_by_class(identifier)
    return render_template(r"Registered.html", name=user_info[0], account_no=identifier, password=user_info[1])


@app.route('/register', methods=['POST', 'GET'])
def register():
    expected_inputs = ["nm", "pw"]
    user_input = [request.form.get(name) if request.method == 'POST' else request.args.get(name)
                  for name in expected_inputs]

    print(user_input)
    identifier = new_account_by_class(user_input[0], user_input[1], 1, [])

    return redirect(url_for("success", identifier=identifier))


if __name__ == '__main__':
    # Your file path will be different from mine. Right click main.html -> copy Path/Reference -> Absolute Path.
    # Then replace the string below. Put r in front of the string to tell python it is a file path.
    webbrowser.open_new_tab(r"C:\Users\Declan\PycharmProjects\flaskthingy\templates\main.html")
    # Webpage will open twice if debug = True.

    app.run(debug=True)



