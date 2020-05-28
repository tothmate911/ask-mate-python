from flask import Flask, render_template, redirect, request, url_for, session, escape, make_response
import data_handler
import database_manager
import password_handler
import os
import utility
from werkzeug.utils import secure_filename
from datetime import datetime

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'


@app.route('/')
def main_page():
    user = password_handler.get_logged_in_user()

    order_by = request.args.get('order_by', 'submission_time')
    order_direction = request.args.get('order_direction', 'desc')
    tags = database_manager.all_tag()
    first_five_sorted_questions_with_reputation = database_manager.get_five_latest_questions_sorted_with_reputation(
        order_by, order_direction)
    return render_template("lists.html",
                           question=first_five_sorted_questions_with_reputation,
                           order_by=order_by,
                           order_direction=order_direction,
                           tags=tags,
                           user=user)


@app.route('/lists')
def route_lists():
    user = password_handler.get_logged_in_user()

    order_by = request.args.get('order_by', 'submission_time')
    order_direction = request.args.get('order_direction', 'asc')
    tags = database_manager.all_tag()
    sorted_questions_with_reputation = database_manager.get_all_questions_sorted_with_reputation(order_by,
                                                                                                 order_direction)
    return render_template("lists.html",
                           question=sorted_questions_with_reputation,
                           order_by=order_by,
                           order_direction=order_direction,
                           tags=tags,
                           user=user)


@app.route('/add_question', methods=['GET', 'POST'])
def route_new_question():
    user = password_handler.get_logged_in_user()
    if user is None:
        return redirect('/')
    if request.method == 'POST':
        new_question = {'submission_time': datetime.now(),
                        'title': request.form.get('title'),
                        'message': request.form.get('message'),
                        'view_number': request.form.get('view_number'),
                        'vote_number': request.form.get('vote_number'),
                        'image': request.form.get('image'),
                        'username': user}
        if request.files['image'].filename != "":

            image = request.files['image']
            if not data_handler.allowed_image(image.filename):
                return redirect(request.url)
            else:
                filename = secure_filename(image.filename)

                image.save(os.path.join(data_handler.IMAGE_UPLOAD_PATH, filename))
                new_question.update({'image': f"{data_handler.IMAGE_UPLOAD_PATH}/{image.filename}"})
        new_question = data_handler.apostroph_change(new_question)
        database_manager.add_question(new_question)
        return redirect('/lists')

    return render_template("add_question.html",
                           comment_name='Add new question',
                           form_url=url_for('route_new_question'),
                           comment_title='Question title',
                           comment_message='Question message',
                           type='question',
                           user=user)


@app.route('/view_up/<question_id>')
def view_up(question_id):
    question = database_manager.get_question_by_id(question_id)[0]
    question['view_number'] = question['view_number'] + 1
    database_manager.view_up(question['id'])
    return redirect(f'/question/{question_id}')


@app.route('/question/<question_id>')
def route_question(question_id):
    user = password_handler.get_logged_in_user()

    vote_ok = request.args.get('vote_ok', None)

    question_with_reputation = database_manager.get_question_by_id_with_reputation(question_id)
    order_by = request.args.get('order_by', 'submission_time')
    order_direction = request.args.get('order_direction', 'asc')
    sorted_answers_with_reputation = database_manager.get_all_answer_by_question_id_sorted_with_reputation(question_id,
                                                                                                           order_by,
                                                                                                           order_direction)

    question_comment_with_reputation = database_manager.get_all_comment_from_question_id_with_reputation(question_id)
    answer_comment_with_reputation = database_manager.get_all_comment_from_answer_id_with_reputation(question_id)
    tags = database_manager.all_tag()
    return render_template("answer.html",
                           question=question_with_reputation,
                           answer=sorted_answers_with_reputation,
                           question_comment=question_comment_with_reputation,
                           answer_comment=answer_comment_with_reputation,
                           order_by=order_by,
                           order_direction=order_direction,
                           tags=tags,
                           user=user,
                           vote_ok=vote_ok)


@app.route('/question/<question_id>/<image>')
def full_screen(question_id, image):
    image_route = '/' + data_handler.ROOT_PATH + '/' + image
    return render_template('full_image.html',
                           image=image_route,
                           question_id=question_id)


@app.route('/question/<question_id>/new-answer', methods=['GET', 'POST'])
def route_new_answer(question_id):
    user = password_handler.get_logged_in_user()
    if user is None:
        return redirect('/')
    if request.method == 'POST':
        new_answer = {'message': request.form.get('message'),
                      'vote_number': request.form.get('vote_number'),
                      'image': request.form.get('image'),
                      'question_id': request.form.get('question_id'),
                      'submission_time': datetime.now(),
                      'username': user}
        if request.files['image'].filename != "":
            image = request.files['image']
            if not data_handler.allowed_image(image.filename):
                return redirect(request.url)
            else:
                filename = secure_filename(image.filename)

                image.save(os.path.join(data_handler.IMAGE_UPLOAD_PATH, filename))
                new_answer.update({'image': f"{data_handler.IMAGE_UPLOAD_PATH}/{image.filename}"})
        new_answer = data_handler.apostroph_change(new_answer)
        database_manager.add_answer(new_answer)
        return redirect(f'/question/{question_id}')

    return render_template("add_question.html",
                           type='answer',
                           comment_name='Add new answer',
                           form_url=url_for('route_new_answer', question_id=question_id),
                           comment_message='Answer message',
                           question_id=question_id,
                           user=user)


@app.route('/question/<question_id>/delete')
def delete_question(question_id):
    user = password_handler.get_logged_in_user()
    question_owner = database_manager.get_question_by_id(question_id)[0]['username']
    if user is None or user != question_owner:
        return redirect('/')
    data_handler.delete_image_by_id(question_id)
    database_manager.delete_question(question_id)
    return redirect('/lists')


@app.route('/answer/<answer_id>/delete')
def delete_answer(answer_id):
    user = password_handler.get_logged_in_user()
    answer_owner = database_manager.get_answer_by_id(answer_id)[0]['username']
    if user is None or user != answer_owner:
        return redirect('/')
    question_id = database_manager.get_answer_by_id(answer_id)[0]['question_id']
    data_handler.delete_image_by_id(answer_id, answer=True)
    database_manager.delete_answer(answer_id)
    return redirect(f'/question/{question_id}')


@app.route('/question/<question_id>/vote_up')
def question_vote_up(question_id):
    user = password_handler.get_logged_in_user()
    if user is None:
        return redirect('/')

    current_user_vote_for_question = database_manager.get_user_vote_for_question(user, question_id)
    if current_user_vote_for_question is None:
        database_manager.add_user_vote_for_question(user, question_id, 1)
        database_manager.vote(question_id, type='question', vote='+')
    elif current_user_vote_for_question < 1:
        new_user_vote_for_question = current_user_vote_for_question + 1
        database_manager.update_user_vote_for_question(user, question_id, new_user_vote_for_question)
        database_manager.vote(question_id, type='question', vote='+')
    else:
        vote_ok = False
        return redirect(url_for('route_question', question_id=question_id, vote_ok=vote_ok))

    question_owner = database_manager.get_question_by_id(question_id)[0]['username']
    database_manager.update_reputation(question_owner)

    return redirect(url_for('route_question', question_id=question_id))


@app.route('/question/<question_id>/vote_down')
def question_vote_down(question_id):
    user = password_handler.get_logged_in_user()
    if user is None:
        return redirect('/')

    current_user_vote_for_question = database_manager.get_user_vote_for_question(user, question_id)
    if current_user_vote_for_question is None:
        database_manager.add_user_vote_for_question(user, question_id, -1)
        database_manager.vote(question_id, type='question', vote='-')
    elif current_user_vote_for_question > -1:
        new_user_vote_for_question = current_user_vote_for_question - 1
        database_manager.update_user_vote_for_question(user, question_id, new_user_vote_for_question)
        database_manager.vote(question_id, type='question', vote='-')

    question_owner = database_manager.get_question_by_id(question_id)[0]['username']
    database_manager.update_reputation(question_owner)

    return redirect(url_for('route_question', question_id=question_id))


@app.route('/answer/<answer_id>/vote_up')
def answer_vote_up(answer_id):
    user = password_handler.get_logged_in_user()
    if user is None:
        return redirect('/')
    question = database_manager.get_answer_by_id(answer_id)
    question_id = question[0]['question_id']

    current_user_vote_for_answer = database_manager.get_user_vote_for_answer(user, answer_id)
    if current_user_vote_for_answer is None:
        database_manager.add_user_vote_for_answer(user, answer_id, 1)
        database_manager.vote(answer_id, type='answer', vote='+')
    elif current_user_vote_for_answer < 1:
        new_user_vote_for_answer = current_user_vote_for_answer + 1
        database_manager.update_user_vote_for_answer(user, answer_id, new_user_vote_for_answer)
        database_manager.vote(answer_id, type='answer', vote='+')

    answer_owner = database_manager.get_answer_by_id(answer_id)[0]['username']
    database_manager.update_reputation(answer_owner)

    return redirect(f'/question/{question_id}')


@app.route('/answer/<answer_id>/vote_down')
def answer_vote_down(answer_id):
    user = password_handler.get_logged_in_user()
    if user is None:
        return redirect('/')
    answer = database_manager.get_answer_by_id(answer_id)
    question_id = answer[0]['question_id']

    current_user_vote_for_answer = database_manager.get_user_vote_for_answer(user, answer_id)
    if current_user_vote_for_answer is None:
        database_manager.add_user_vote_for_answer(user, answer_id, -1)
        database_manager.vote(answer_id, type='answer', vote='-')
    elif current_user_vote_for_answer > -1:
        new_user_vote_for_answer = current_user_vote_for_answer - 1
        database_manager.update_user_vote_for_answer(user, answer_id, new_user_vote_for_answer)
        database_manager.vote(answer_id, type='answer', vote='-')

    answer_owner = database_manager.get_answer_by_id(answer_id)[0]['username']
    database_manager.update_reputation(answer_owner)

    return redirect(f'/question/{question_id}')


@app.route('/question/<question_id>/edit', methods=['GET', 'POST'])
def edit_question(question_id):
    user = password_handler.get_logged_in_user()
    question_owner = database_manager.get_question_by_id(question_id)[0]['username']
    if user is None or user != question_owner:
        return redirect('/')
    question = database_manager.get_question_by_id(question_id)[0]
    if request.method == 'POST':
        datas_from_edit = ['title', 'message']
        for data in datas_from_edit:
            question[data] = request.form[data]
        question['submission_time'] = datetime.now()
        question['accepted_answer_id'] = 'null'
        question = data_handler.apostroph_change(question)
        database_manager.update_question(question)
        return redirect(url_for('route_question', question_id=question_id))

    return render_template('edit_answer.html',
                           question=question,
                           from_url=url_for('edit_question', question_id=question_id),
                           type='question',
                           user=user)


@app.route('/answer/<answer_id>/edit', methods=['GET', 'POST'])
def edit_answer(answer_id):
    user = password_handler.get_logged_in_user()
    answer_owner = database_manager.get_answer_by_id(answer_id)[0]['username']
    if user is None or user != answer_owner:
        return redirect('/')
    answer = database_manager.get_answer_by_id(answer_id)[0]
    if request.method == 'POST':
        datas_from_edit = ['message']
        for data in datas_from_edit:
            answer[data] = request.form[data]
        answer['submission_time'] = datetime.now()
        answer = data_handler.apostroph_change(answer)
        database_manager.update_answer(answer, answer_id)
        return redirect(url_for('route_question', question_id=answer['question_id']))

    return render_template('edit_answer.html',
                           answer=answer,
                           from_url=url_for('edit_answer', answer_id=answer_id),
                           user=user)


@app.route('/search')
def route_search():
    user = password_handler.get_logged_in_user()
    if user is None:
        return redirect('/')
    search_phrase = request.args.get('search')
    questions_with_reputation = database_manager.search_in_questions_with_reputation(search_phrase)
    data_handler.remove_from_list(questions_with_reputation)
    questions_with_reputation = data_handler.search_highlight(questions_with_reputation, search_phrase)
    answers_with_reputation = database_manager.search_in_answers_with_reputation(search_phrase)
    answers_with_reputation = data_handler.search_highlight(answers_with_reputation, search_phrase)
    tags = database_manager.all_tag()
    tags = data_handler.search_highlight(tags, search_phrase)
    return render_template('Search.html',
                           question=questions_with_reputation,
                           answer=answers_with_reputation,
                           type='search',
                           search_word=search_phrase,
                           tags=tags,
                           user=user)


@app.route('/question/<question_id>/new_comment', methods=['GET', 'POST'])
def add_new_comment_to_question(question_id):
    user = password_handler.get_logged_in_user()
    if user is None:
        return redirect('/')
    if request.method == 'POST':
        database_manager.write_new_comment(request.form.to_dict())
        return redirect(f'/question/{question_id}')

    return render_template("new_comment.html",
                           comment_name='Add Comment',
                           form_url=url_for('add_new_comment_to_question', question_id=question_id),
                           comment_message='Add Comment',
                           question_id=question_id,
                           user=user)


@app.route('/answer/<answer_id>/new_comment', methods=['GET', 'POST'])
def add_new_comment_to_answer(answer_id):
    user = password_handler.get_logged_in_user()
    if user is None:
        return redirect('/')
    question_id = database_manager.get_answer_by_id(answer_id)[0]['question_id']
    if request.method == 'POST':
        database_manager.write_new_comment(request.form.to_dict())
        return redirect(f'/question/{question_id}')

    return render_template("new_comment.html",
                           comment_name='Add Comment',
                           type='answer',
                           form_url=url_for('add_new_comment_to_answer', answer_id=answer_id),
                           comment_message='Add Comment',
                           answer_id=answer_id,
                           question_id=question_id,
                           user=user)


@app.route('/comment/<comment_id>/edit', methods=['GET', 'POST'])
def edit_comment(comment_id):
    user = password_handler.get_logged_in_user()
    comment_owner = database_manager.get_answer_by_id(comment_id)[0]['username']
    if user is None or user != comment_owner:
        return redirect('/')
    comment = database_manager.get_comment_by_id(comment_id)[0]
    if request.method == 'POST':
        datas_from_edit = ['message']
        for data in datas_from_edit:
            comment[data] = request.form[data]
        comment['submission_time'] = datetime.now()
        comment = data_handler.apostroph_change(comment)
        database_manager.update_comment(comment, comment_id)
        return redirect(url_for('route_question', question_id=comment['question_id']))

    return render_template('edit_answer.html',
                           comment=comment,
                           type='comment',
                           from_url=url_for('edit_comment', comment_id=comment_id),
                           user=user)


@app.route('/comment/<comment_id>/delete')
def delete_comment(comment_id):
    user = password_handler.get_logged_in_user()
    comment_owner = database_manager.get_answer_by_id(comment_id)[0]['username']
    if user is None or user != comment_owner:
        return redirect('/')
    comment = database_manager.get_comment_by_id(comment_id)[0]
    database_manager.delete_comment(comment_id)
    return redirect(url_for('route_question', question_id=comment['question_id']))


@app.route('/question/<question_id>/new_tag', methods=['GET', 'POST'])
def add_tag(question_id):
    user = password_handler.get_logged_in_user()
    question_owner = database_manager.get_question_by_id(question_id)[0]['username']
    if user is None or user != question_owner:
        return redirect('/')
    all_tag = database_manager.all_tag_name()
    if request.method == 'POST':
        tag = {}
        new_tag = request.form.get('new_tag')
        old_tag = request.form.get('use_tag')
        if new_tag is not '':
            tag['name'] = new_tag
            duplicate = data_handler.tag_duplicate_check(new_tag)
            if duplicate:
                database_manager.add_old_tag(tag, question_id)
            else:
                database_manager.add_tag(tag, question_id)
        else:
            tag['name'] = old_tag
            database_manager.add_old_tag(tag, question_id)
        return redirect(f'/question/{question_id}')

    return render_template('add_tag.html',
                           question_id=question_id,
                           tags=all_tag,
                           user=user)


@app.route('/question/<question_id>/tag/<tag_id>/delete')
def delete_tag(question_id, tag_id):
    user = password_handler.get_logged_in_user()
    question_owner = database_manager.get_answer_by_id(question_id)[0]['username']
    if user is None or user != question_owner:
        return redirect('/')
    database_manager.delete_tag(tag_id, question_id)
    return redirect(f'/question/{question_id}')


@app.route('/tag/search/<tag_id>')
def search_with_tag(tag_id):
    user = password_handler.get_logged_in_user()
    if user is None:
        return redirect('/')
    questions_by_tag_id = database_manager.all_question_by_tag_id(tag_id)
    tags = database_manager.all_tag()
    tag = database_manager.tag_by_tag_id(tag_id)[0]
    tags = data_handler.search_highlight(tags, tag['name'])
    return render_template('Search.html',
                           question=questions_by_tag_id,
                           tag=tag,
                           tags=tags,
                           user=user)


@app.route('/all_user')
def all_user():
    user = password_handler.get_logged_in_user()
    users = database_manager.all_user()
    return render_template('list_users.html',
                           users=users,
                           user=user)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        login_username = request.form.get('username')
        login_plain_text_password = request.form.get('password')
        try:
            hashed_pw_for_login_username = database_manager.get_hashed_pw_for_username(login_username)
            password_is_ok = password_handler.verify_password(login_plain_text_password, hashed_pw_for_login_username)
            if password_is_ok is True:
                session['username'] = login_username
                return redirect(url_for('route_lists'))
        except:
            return render_template('registration.html',
                                   user=None,
                                   message=True)

    return render_template('registration.html',
                           user=None,
                           message=False)


@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('route_lists'))


@app.route('/registration', methods=['GET', 'POST'])
def registration():
    if request.method == 'POST':
        registration_username = request.form.get('username')
        hashed_pw = utility.hash_password(request.form.get('password'))
        users = database_manager.all_user()
        for user in users:
            if user['user_name'] == registration_username:
                return render_template('registration.html',
                                       type='registration',
                                       message='registration fail')
        database_manager.member_registration(registration_username, hashed_pw)
        # session['username'] = registration_username

        return redirect('/')

    return render_template('registration.html',
                           type='registration')


@app.route('/user/<user_name>')
def user_page(user_name):
    user = password_handler.get_logged_in_user()
    if user is None:
        return redirect('/')
    datas = {}
    datas['tag'] = database_manager.all_tag()
    datas['user_name'] = user_name
    datas['question'] = database_manager.question_of_user_with_reputation(user_name)
    datas['answer'] = database_manager.answer_of_user_with_reputation(user_name)
    datas['comment'] = database_manager.comment_of_user_with_reputation(user_name)
    return render_template('user_page.html',
                           data=datas,
                           user=user)


@app.route('/accepted_answer/<question_id>/<answer_id>')
def accept_answer(question_id, answer_id):
    user = password_handler.get_logged_in_user()
    if user is None:
        return redirect('/')
    question = database_manager.get_question_by_id(question_id)[0]
    question['accepted_answer_id'] = answer_id
    database_manager.update_question(question)

    accepted_answer_owner = database_manager.get_answer_by_id(answer_id)[0]['username']
    database_manager.update_reputation(accepted_answer_owner)

    return redirect(f'/question/{question_id}')


@app.route('/accepted_answer/cancel/<question_id>/')
def cancel_answer(question_id):
    user = password_handler.get_logged_in_user()
    if user is None:
        return redirect('/')
    question = database_manager.get_question_by_id(question_id)[0]

    answer_id_to_be_canceled = question['accepted_answer_id']

    question['accepted_answer_id'] = 'null'
    database_manager.update_question(question)

    canceled_answer_owner = database_manager.get_answer_by_id(answer_id_to_be_canceled)[0]['username']
    database_manager.update_reputation(canceled_answer_owner)

    # TODO url_for
    return redirect(f'/question/{question_id}')


if __name__ == "__main__":
    app.run(
        host='0.0.0.0',
        port=8000,
        debug=True,
    )
