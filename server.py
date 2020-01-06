from flask import Flask, render_template, redirect, request, url_for
import data_handler
import database_manager
import os
from werkzeug.utils import secure_filename
app = Flask(__name__)


@app.route('/')
@app.route('/lists')
def route_lists():
    questions = data_handler.get_all_questions()
    try:
        order_by = request.args['order_by']
        order_direction = request.args['order_direction']
    except:
        order_by = 'submission_time'
        order_direction = 'asc'

    sorted_questions = data_handler.sort_data(questions, order_by, order_direction)
    return render_template("lists.html", question=sorted_questions, order_by=order_by, order_direction=order_direction)


@app.route('/add_question', methods=['GET', 'POST'])
def route_new_question():
    if request.method == 'POST':
        comment = {'title': request.form.get('title'),
                   'message': request.form.get('message'),
                   'submission_time': request.form.get('submission_time'),
                   'view_number': request.form.get('view_number'),
                   'vote_number': request.form.get('vote_number'),
                   }
        if request.files['image'].filename != "":

            image = request.files['image']
            if not data_handler.allowed_image(image.filename):
                return redirect(request.url)
            else:
                filename = secure_filename(image.filename)

                image.save(os.path.join(data_handler.IMAGE_UPLOAD_PATH, filename))
                comment.update({'image': f"{data_handler.IMAGE_UPLOAD_PATH}/{image.filename}"})

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
    print(question['image'])
    answers = data_handler.all_answer_for_one_question(question_id)
    try:
        order_by = request.args['order_by']
        order_direction = request.args['order_direction']
    except:
        order_by = 'submission_time'
        order_direction = 'asc'
    sorted_answers = data_handler.sort_data(answers, order_by, order_direction)

    return render_template("answer.html",
                           question=question,
                           answer=sorted_answers, order_by=order_by, order_direction=order_direction)


@app.route('/question/<question_id>/new-answer', methods=['GET', 'POST'])
def route_new_answer(question_id):
    if request.method == 'POST':
        comment = {'message': request.form.get('message'),
                   'submission_time': request.form.get('submission_time'),
                   'vote_number': request.form.get('vote_number'),
                   'image': request.form.get('image'),
                   'question_id': request.form.get('question_id')}
        data_handler.add_answer(comment, question_id)
        return redirect(f'/question/{question_id}')

    return render_template("add_question.html",
                           type='answer',
                           comment_name='Add new answer',
                           form_url=url_for('route_new_answer', question_id=question_id),
                           comment_message='Answer message',
                           question_id=question_id,
                           timestamp=data_handler.date_time_in_timestamp())

@app.route('/question/<question_id>/delete')
def delete_question(question_id):
    data_handler.delete_image_by_question_id(question_id)
    data_handler.delete_question(question_id)
    data_handler.delete_answers_by_question_id(question_id)
    return redirect('/lists')

@app.route('/answer/<answer_id>/delete')
def delete_answer(answer_id):
    questionid = data_handler.search_question_id_by_answer(answer_id)
    data_handler.delete_specific_answer(answer_id)
    return redirect(f'/question/{questionid}')


@app.route('/question/<question_id>/vote_up')
def question_vote_up(question_id):
    data_handler.vote(question_id)
    return redirect(f'/question/{question_id}')


@app.route('/question/<question_id>/vote_down')
def question_vote_down(question_id):
    data_handler.vote(question_id, type_vote_up=False)
    return redirect(f'/question/{question_id}')


@app.route('/answer/<answer_id>/vote_up')
def answer_vote_up(answer_id):
    data_handler.vote(answer_id, question_type=False)
    question_id = data_handler.search_question_id_by_answer(answer_id)
    return redirect(f'/question/{question_id}')


@app.route('/answer/<answer_id>/vote_down')
def answer_vote_down(answer_id):
    question_id = data_handler.search_question_id_by_answer(answer_id)
    data_handler.vote(answer_id, question_type=False, type_vote_up=False)
    return redirect(f'/question/{question_id}')


@app.route('/question/<question_id>/edit',methods = ['GET', 'POST'])
def edit_question(question_id):
    question = data_handler.get_question_by_id(question_id)
    if request.method == 'POST':
        edited_question = {}
        datas_from_question = ['id', 'submission_time', 'view_number', 'vote_number', 'image']
        for data in datas_from_question:
            edited_question[data] = question[data]
        datas_from_edit = ['title', 'message']
        for data in datas_from_edit:
            edited_question[data] = request.form[data]

        data_handler.update_question(edited_question)
        return redirect(url_for('route_question', question_id=edited_question['id']))

    return render_template('edit_question.html', question=question)


@app.route('/answer/<answer_id>/edit', methods=['GET', 'POST'])
def edit_answer(answer_id):
    answer = data_handler.get_answer_by_id(answer_id)
    if request.method == 'POST':
        edited_answer = {}
        datas_from_answer = ['id', 'submission_time', 'vote_number', 'question_id', 'image']
        for data in datas_from_answer:
            edited_answer[data] = answer[data]
        datas_from_edit = ['message']
        for data in datas_from_edit:
            edited_answer[data] = request.form[data]

        data_handler.update_answer(edited_answer)
        return redirect(url_for('route_question', question_id=edited_answer['question_id']))

    return render_template('edit_answer.html', answer=answer)


if __name__ == "__main__":
    app.run(
        host='0.0.0.0',
        port=8000,
        debug=True,
        )
