from flask import Flask, render_template, redirect, request, url_for
import data_handler
app = Flask(__name__)

@app.route('/')
@app.route('/lists')
def route_lists():
    questions = data_handler.get_all_questions()
    return render_template('lists.html', question=questions)

@app.route('/add_question', methods=['GET', 'POST'])
def route_edit():
    if request.method == 'POST':
        question = {}
        for titles in data_handler.DATA_HEADER[1:]:
            question.update({titles: request.form.get[titles]})
        data_handler.add_question(question)
        return redirect('/lists'),

    return render_template('add_question.html',
                           comment_name='Add new question',
                           form_url=url_for('new_question_add'),
                           comment_title='Question title',
                           comment_message='Question message')

if __name__ == "__main__":
    app.run(
        host='0.0.0.0',
        port=8000,
        debug=True,
        )
