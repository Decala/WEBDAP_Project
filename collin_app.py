from flask import Flask, redirect, url_for, session, render_template, request, jsonify
from steps_data import steps_data
import shelve
from chatbot_dictionary import responses


app = Flask(__name__)
app.secret_key = 'seizuresmart-key'


@app.route("/")
def home():
    return render_template("home.html")


@app.route('/chatbot')
def chatbot():
    lang = request.args.get('lang')
    if lang:
        session['chat_lang'] = lang  # save language in session
    return render_template('chatbot.html')


@app.route("/video")
def video():
    section = request.args.get("section", "")
    return render_template("video.html", section=section)


@app.route("/infographic")
def infographic():
    section = request.args.get("section", "")
    return render_template("infographic.html", section=section)


@app.route("/cards")
def cards():
    section = request.args.get("section", "")
    return render_template("cards.html", section=section)


@app.route('/quiz', methods=['GET', 'POST'])
def quiz():
    with shelve.open("quiz_db") as db:
        questions = db["questions"]

    if "current_q" not in session:
        session["current_q"] = 0
        session["score"] = 0

    current_q = session["current_q"]
    feedback = None

    if request.method == 'POST':
        selected = request.form.get("answer")
        correct_answer = questions[current_q]["answer"]

        if selected == correct_answer:
            session["score"] += 1
            session["current_q"] += 1
            feedback = "Correct!"
        else:
            feedback = "Wrong! Try again."

        current_q = session["current_q"]

    if current_q >= len(questions):
        score = session["score"]
        session.clear()
        return render_template("quiz_result.html", score=score, total=len(questions))

    question = questions[current_q]
    return render_template("quiz.html", question=question, q_num=current_q + 1, total=len(questions), feedback=feedback)


@app.route('/chatbot_api', methods=['POST'])
def chatbot_api():
    # Chatbot responses from chatbot_dictionary.py
    data = request.get_json()
    user_message = data.get('message', '').lower()

    # Check for keyword match
    reply = None
    for keyword, current_response in responses.items():
        if keyword in user_message:
            reply = current_response["en"]
            break

    # Default fallback message
    if not reply:
        reply = "I'm still learning. Try keywords like 'seizure', 'steps', or 'symptoms'."

    return jsonify({"reply": reply})


@app.route("/learn")
def learn():
    return render_template("learn.html")


@app.route("/guide")
def start_guide():
    lang = request.args.get("lang", "en")
    autoplay = request.args.get("autoplay", "false")
    handsfree = request.args.get("handsfree", "false")
    return redirect(url_for("guide_step", step_num=1, lang=lang, autoplay=autoplay, handsfree=handsfree))


@app.route("/guide/<int:step_num>")
def guide_step(step_num):
    lang = request.args.get("lang", "en")
    autoplay = request.args.get("autoplay", "false")
    handsfree = request.args.get("handsfree", "false")
    if 1 <= step_num <= len(steps_data):
        step = steps_data[step_num - 1]
        audio_file = step["audio"].get(lang, step["audio"]["en"])
        return render_template("guide_step.html",
                               step=step,
                               lang=lang,
                               audio_file=audio_file,
                               autoplay=autoplay,
                               handsfree=handsfree,
                               current_step=step_num,
                               total_steps=len(steps_data))
    return "Step not found", 404


@app.route("/education")
def education():
    return render_template("education.html")


if __name__ == "__main__":
    app.run(debug=True)
