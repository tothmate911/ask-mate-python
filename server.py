from flask import Flask, render_template, redirect, request, url_for
import data_handler
app = Flask(__name__)


@app.route('/')
@app.route('/list')
def route_index():
    all_questions = data_handler.get_all_questions()
    return render_template('lists.html', all_questions=all_questions)


@app.route('/add_question', methods=['GET', 'POST'])
def add_question():
    if request.method == 'POST':
        question = {}
        for title in data_handler.QUESTION_DATA_HEADER[1:]:
            question.update({title: request.form[title]})
        data_handler.add_question(question)
        return redirect('/')

    return render_template('add_question.html')


@app.route('/question/<question_id>', methods=['GET', 'POST'])
def show_question(question_id):
    question = data_handler.get_question_by_id(question_id)
    answers_for_question = data_handler.get_all_answers_for_a_question(question_id)
    return render_template('show_question.html', question=question, answers_for_question=answers_for_question)


if __name__ == "__main__":
    app.run(
        host='0.0.0.0',
        port=8000,
        debug=True,
        )
