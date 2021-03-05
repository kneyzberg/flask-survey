from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey

app = Flask(__name__)
app.config['SECRET_KEY'] = "never-tell!"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)


@app.route("/")
def index():
    title = survey.title
    instructions = survey.instructions
    session["responses"] = []
    
    return render_template("survey_start.html", survey_title=title, 
    survey_instructions=instructions)

@app.route("/begin", methods=["POST"])
def begin():
    return redirect("/questions/0")

@app.route("/questions/<int:index>")
def questions(index):
    question = survey.questions[index]
    session["questions"] = 0
    session["questions"] = index
    print(f"\n\n session question = {session['questions']}")

    if index > len(session["responses"]):
        return redirect(f"/questions/{len(session['responses'])}")

    return render_template("question.html",question =question)


@app.route("/answer", methods=["POST"])
def answer():
    response = {}
    response[session["questions"]] = request.form["answer"]

    responses = session["responses"]
    print(f"\n\n response = {response}")
    responses.append(response)
    session["responses"] = responses
    print(f"\n\nresponses: {responses}")
    print(f"\n\nsesssion responses: {session['responses']}")

    length = len(responses)
    
    if length < len(survey.questions):
        return redirect(f"/questions/{length}")

    return redirect("/thankyou")

@app.route("/thankyou")
def thank_you():
    return render_template("completion.html")