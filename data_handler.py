import csv

ANSWER_FILE_PATH = '/home/bala/Documents/Codecool/Web/ask-mate-python/sample_data/answer.csv'
QUESTION_FILE_PATH = '/home/bala/Documents/Codecool/Web/ask-mate-python/sample_data/question.csv'
ANSWER_DATA_HEADER = ['id', 'submission_time', 'vote_number', 'question_id', 'message', 'image']
QUESTION_DATA_HEADER = ['id', 'submission_time', 'view_number', 'vote_number', 'title', 'message', 'image']


def get_all_questions():
    all_questions = get_list_of_dictionaries_from_csv(QUESTION_FILE_PATH, QUESTION_DATA_HEADER)
    return all_questions


def get_all_answers():
    all_answers = get_list_of_dictionaries_from_csv(ANSWER_FILE_PATH, ANSWER_DATA_HEADER)
    return all_answers


def get_list_of_dictionaries_from_csv(path, actual_data_header):
    with open(path) as csvfile:
        reader = csv.DictReader(csvfile, fieldnames=actual_data_header)
        all_data = [data for data in reader]
    return all_data


def get_question_by_id(question_id):
    all_questions = get_all_questions()
    for question in all_questions:
        if question['id'] == question_id:
            return question


def get_all_answers_for_a_question(question_id):
    all_answers = get_all_answers()
    answers_for_a_question = [answer for answer in all_answers if answer['question_id'] == question_id]
    return answers_for_a_question


def next_id_generator(path):
    actual_data_header = []
    if path == QUESTION_FILE_PATH:
        actual_data_header = QUESTION_DATA_HEADER
    elif path == ANSWER_FILE_PATH:
        actual_data_header = ANSWER_DATA_HEADER
    data = get_list_of_dictionaries_from_csv(path, actual_data_header)
    try:
        next_id = int(data[-1]['id']) + 1
    except ValueError:
        next_id = 0
    return next_id


def add_question(quiestion_to_add):
    with open(QUESTION_FILE_PATH, 'a') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=QUESTION_DATA_HEADER)
        writer.writerow(quiestion_to_add)
    pass


def add_answer(answer_to_add):
    with open(ANSWER_FILE_PATH, 'a') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=ANSWER_DATA_HEADER)
        writer.writerow(answer_to_add)
    pass
