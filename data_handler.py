import csv

ANSWER_FILE_PATH = 'sample_data/answer.csv'
QUESTION_FILE_PATH = 'sample_data/question.csv'
DATA_HEADER =['id', 'submission_time', 'view_number', 'vote_number', 'title', 'message', 'image']


def get_all_questions():
    all_questions = get_list_of_dictionaries_from_csv(QUESTION_FILE_PATH)
    return all_questions


def get_all_answers():
    all_answers = get_list_of_dictionaries_from_csv(ANSWER_FILE_PATH)
    return all_answers


def get_list_of_dictionaries_from_csv(path):
    with open(path) as csvfile:
        reader = csv.DictReader(csvfile, fieldnames=DATA_HEADER)
        all_data = []
        for data in reader:
            if data['id'] != 'id':
                all_data.append(data)
    return all_data


def get_question_by_id(id):
    all_questions = get_all_questions()
    for question in all_questions:
        if question['id'] == id:
            return question


def next_id_generator(path):
    data = get_list_of_dictionaries_from_csv(path)
    try:
        next_id = int(data[-1]['id']) + 1
    except ValueError:
        next_id = 0
    return next_id

def add_question(question):
    question['id'] = next_id_generator(question)
    write_the_file(QUESTION_FILE_PATH, question, append=True)

def write_the_file(file_name, write_elements, append=True):
    existing_data = get_all_questions()
    with open(file_name, 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=DATA_HEADER)
        writer.writeheader()

        for row in existing_data:
            if not append:
                if row['id'] == write_elements['id']:
                    row = write_elements

            writer.writerow(row)

        if append:
            writer.writerow(write_elements)

def one_question(question_id):
    all_question = get_all_questions()
    for question in all_question:
        if question['id'] == question_id:
            return question

def all_answer_for_one_question(question_id):
    answers = []
    all_answer = get_all_answers()
    for answer in all_answer:
        if answer['question_id'] == question_id:
            answers.append(answer)
    return answers
