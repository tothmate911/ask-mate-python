from flask import Flask, render_template, redirect, request, url_for
import data_handler
app = Flask(__name__)

@app.route('/')
@app.route('/lists')
def route_lists():
    questions = data_handler.get_all_questions(time=True)
    return render_template("lists.html", question=questions)

@app.route('/add_question', methods=['GET', 'POST'])
def route_new_question():
    if request.method == 'POST':
        comment = {'title': request.form.get('title'),
                   'message': request.form.get('message'),
                   'submission_time': request.form.get('submission_time'),
                   'view_number': request.form.get('view_number'),
                   'vote_number': request.form.get('vote_number'),
                   'image': request.form.get('image')}
        data_handler.add_question(comment)
        return redirect('/lists')

    return render_template("add_question.html",
                           comment_name='Add new question',
                           form_url=url_for('route_new_question'),
                           comment_title='Question title',
                           comment_message='Question message',
                           type='question')

@app.route('/question/<question_id>')
def route_question(question_id):
    question = data_handler.one_question(question_id, time=True)
    answer = data_handler.all_answer_for_one_question(question_id)
    return render_template("answer.html",
                           question=question,
                           answer=answer)

@app.route('/question/<question_id>/new-answer', methods=['GET', 'POST'])
def route_new_answer(question_id):
    if request.method == 'POST':
        comment = {'message': request.form.get('message'),
                   'submission_time': request.form.get('submission_time'),
                   'vote_number': request.form.get('vote_number'),
                   'image': request.form.get('image'),
                   'question_id': request.form.get('question_id')}
        page_return = f'/question/{question_id}'
        data_handler.add_answer(comment, question_id)
        return redirect(page_return)

    return render_template("add_question.html",
                           comment_name='Add new answer',
                           form_url=url_for('route_new_answer', question_id=question_id),
                           comment_message='Answer message',
                           question_id=question_id,
                           timestamp=data_handler.date_time_in_timestamp())


if __name__ == "__main__":
    app.run(
        host='0.0.0.0',
        port=8000,
        debug=True,
        )
