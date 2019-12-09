from flask import Flask, render_template, redirect, request
import data_handler
app = Flask(__name__)

@app.route('/')
def route_index():

    return render_template('index.html')

@app.route('/add_question', methods=['GET', 'POST'])
def route_edit():
    if request.method == 'POST':
        question={}

        for titles in data_handler.DATA_HEADER[1:]:
            question.update({titles : request.form[titles]})
        data_handler.add_question(question)
        return redirect('/'),

    return render_template('add_question.html.html')

@app.route('/lists')
def show_questions():
    return render_template('lists.html', data_handler.get_all_questions())

if __name__ == "__main__":
    app.run(
        host='0.0.0.0',
        port=8000,
        debug=True,
        )
