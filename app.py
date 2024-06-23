from flask import Flask, render_template, request, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import Survey, satisfaction_survey

app = Flask(__name__)
app.config['SECRET_KEY'] = 'sEcReTkEy!'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)

# Initialize empty list called 'responses' to store user responses as they progress
responses = []


@app.route('/')
def show_survey():
    """
    Render the initial survey page.
    Display the title, instructions, & start survey button

    Returns:
        show_survey.html template & survey details

    """
    return render_template('show_survey.html', survey=satisfaction_survey)

@app.route('/start', methods=["POST"])
def start_survey():
    """
    Start survey by initializing the session responses.
    Redirect to question/0

    """
    session['responses'] = []
    return redirect('/question/0')


@app.route('/question/<int:question_id>')
def question(question_id):
    """
    Handle the current question details

    """

    # Retrieve the list of responses from the session
    # or use an empty list if not found
    responses = session.get('responses', [])

     # display current question
    question = satisfaction_survey.questions[question_id]

    # user trying to access questions out of order
    if len(responses) != question_id:
        flash(f'Invalid question id: {question_id}.')
        return redirect(f'/question/{len(responses)}')

    return render_template('question.html', question=question, question_id=question_id)


@app.route('/answer', methods=["POST"])
def handle_answer():
    """
    Append response and redirect user to the next question

    """
    # Get the user's name=answer from the form submission
    user_choice = request.form.get('answer')

    # Retrieve the list of responses from the session
    # or use an empty list if not found
    responses = session.get('responses', [])

    # Append the user's answer to the list of responses
    responses.append(user_choice)

    # Store the updated list back in the session
    session['responses'] = responses

    # redirect user to thank_you page if survey is complete
    if len(responses) == len(satisfaction_survey.questions):
        return redirect('/thank_you')
    else:
        # go to next question
        next_question_id = len(responses)
        return redirect(f'/question/{next_question_id}')


@app.route('/thank_you')
def thank_you():
    """
    Display the thank you page

    """
    return render_template('thank_you.html')