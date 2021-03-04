from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey

app = Flask(__name__)
app.config['SECRET_KEY'] = "never-tell!"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)

responses = []
index = 0

@app.route("/")
def index():
    title = survey.title
    instructions = survey.instructions
    return render_template("survey_start.html", survey_title=title, 
    survey_instructions=instructions)

@app.route("/begin", methods=["POST"])
def begin():
    return redirect("/questions/0")

@app.route("/questions/<int:question_number>")
def questions(question_number):
    index = question_number
    question = survey.questions[index]
    return render_template("question.html",question =question)

@app.route("/answer", methods=["POST"])
def answer():
    # index += 1
    print(f"\n{request.form}")
    response = request.form["answer"]
    responses.append(response)
    return redirect("/questions/1")