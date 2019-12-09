import csv

ANSWER_FILE_PATH = 'sample_data/answer.csv'
QUESTION_FILE_PATH = 'sample_data/question.csv'
DATA_HEADER =['id', 'submission_time', 'view_number', 'vote_number', 'title', 'message', 'image']


def get_all_questions():
    all_questions = get_list_of_dictionaries_from_csv(QUESTION_FILE_PATH)
    return  all_questions


def get_all_answers():
    all_answers = get_list_of_dictionaries_from_csv(ANSWER_FILE_PATH)
    return  all_answers


def get_list_of_dictionaries_from_csv(path):
    with open(path) as csvfile:
        reader = csv.DictReader(csvfile, fieldnames=DATA_HEADER)
        all_data = [data for data in reader]
    return all_data


def get_question_by_id(id):
    all_questions = get_all_questions()
    for question in all_questions:
        if question['id'] == id:
            return question
