from flask import Flask, render_template, redirect, request
import data_handler
app = Flask(__name__)

@app.route('/')
def route_index():

    return render_template('index.html')

@app.route('/edit-note', methods=['GET', 'POST'])
def route_edit():
    if request.method == 'POST':


        return redirect('/'),

    return render_template('edit.html')

@app.route('/lists')
def show_questions():
    return render_template('lists.html', data_handler.get_all_questions())

if __name__ == "__main__":
    app.run(
        host='0.0.0.0',
        port=8000,
        debug=True,
        )
