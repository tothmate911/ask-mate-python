import csv
from datetime import datetime
import time

ANSWER_FILE_PATH = 'sample_data/answer.csv'
QUESTION_FILE_PATH = 'sample_data/question.csv'
DATA_HEADER =['id', 'submission_time', 'view_number', 'vote_number', 'title', 'message', 'image']
ANSWER_HEADER =['id', 'submission_time', 'vote_number', 'question_id', 'message', 'image']
IMAGE_UPLOAD_PATH = "static/images"
ALLOWED_IMAGE_TYPE = ["PNG", "JPG"]


def get_all_questions(time=False):
    all_questions = get_list_of_dictionaries_from_csv(QUESTION_FILE_PATH, DATA_HEADER, time)
    return all_questions


def get_all_answers(time=False):
    all_answers = get_list_of_dictionaries_from_csv(ANSWER_FILE_PATH, ANSWER_HEADER, time)
    return all_answers


def get_list_of_dictionaries_from_csv(path, header, time=False):
    with open(path, encoding='utf-8') as csv_file:
        reader = csv.DictReader(csv_file, fieldnames=header)
        all_data = []
        if not time:
            for data in reader:
                if data['id'] != 'id':
                    all_data.append(data)
        else:
            for data in reader:
                if data['id'] != 'id':
                    real_time = datetime.fromtimestamp(int(data['submission_time']))
                    data['submission_time'] = real_time
                    all_data.append(data)
    return all_data


def get_question_by_id(question_id):
    return get_data_by_id(get_all_questions, question_id)


def get_answer_by_id(answer_id):
  return get_data_by_id(get_all_answers, answer_id)


def get_data_by_id(get_all_data, id):
    all_data = get_all_data()
    for data in all_data:
        if data['id'] == id:
            return data


def next_id_generator(path, header):
    data = get_list_of_dictionaries_from_csv(path, header)
    try:
        next_id = int(data[-1]['id']) + 1
    except ValueError:
        next_id = 0
    return next_id

def add_question(question):
    question['id'] = next_id_generator(QUESTION_FILE_PATH, DATA_HEADER)
    question['submission_time'] = date_time_in_timestamp()
    write_the_file(QUESTION_FILE_PATH, question, DATA_HEADER, append=True)

def add_answer(answer, question_id):
    answer['id'] = next_id_generator(ANSWER_FILE_PATH, DATA_HEADER)
    answer['submission_time'] = date_time_in_timestamp()
    answer['question_id'] = question_id
    write_the_file(ANSWER_FILE_PATH, answer, ANSWER_HEADER, append=True)

def write_the_file(file_name, write_elements, header, append=True, delete=False):
    if header == ANSWER_HEADER:
        existing_data = get_all_answers()
    else:
        existing_data = get_all_questions()
    with open(file_name, 'w', encoding='utf-8') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=header)
        writer.writeheader()
        if delete==False:
            for row in existing_data:
                if not append:
                    if row['id'] == write_elements['id']:
                        row = write_elements

                writer.writerow(row)

            if append:
                writer.writerow(write_elements)
        else:
            for element in write_elements:
                writer.writerow(element)

def one_question(question_id, time=False):
    all_question = get_all_questions(time)
    for question in all_question:
        if question['id'] == question_id:
            return question

def all_answer_for_one_question(question_id):
    answers = []
    all_answer = get_all_answers(time=True)
    for answer in all_answer:
        if answer['question_id'] == str(question_id):
            answers.append(answer)
    return answers

def date_time_in_timestamp():
    return int(time.time())

def real_date_time(timestamp):
    return datetime.fromtimestamp(timestamp)

def delete_question(id):
    questions=get_all_questions()
    for each_question in questions:
        if id == each_question['id']:
            questions.remove(each_question)
    write_the_file(QUESTION_FILE_PATH, questions, DATA_HEADER, append=False, delete=True)

def delete_answers_by_question_id(id):
    answers = get_all_answers()
    answers_to_delete=[]
    for each_answer in answers:
        if id == each_answer['question_id']:
            answers_to_delete.append(each_answer)
    for answer in answers_to_delete:
        answers.remove(answer)
    write_the_file(ANSWER_FILE_PATH, answers, ANSWER_HEADER, append=False, delete=True)

def vote(vote_id, question_type=True, type_vote_up=True):
    if question_type:
        all_question = get_all_questions()
    else:
        all_question = get_all_answers()
    for question in all_question:
        if question['id'] == vote_id:
            if type_vote_up:
                question['vote_number'] = str(int(question['vote_number']) + 1)
            else:
                question['vote_number'] = str(int(question['vote_number']) - 1)
            if question_type:
                write_the_file(QUESTION_FILE_PATH, question, DATA_HEADER, append=False)
            else:
                write_the_file(ANSWER_FILE_PATH, question, ANSWER_HEADER, append=False)

def search_question_id_by_answer(answer_id):
    all_answer = get_all_answers()
    question_id = 0
    for answer in all_answer:
        if answer['id'] == answer_id:
            question_id = answer['question_id']
    return question_id

def delete_specific_answer(id):
    answers = get_all_answers()
    for each_answer in answers:
        if id == each_answer['id']:
            answers.remove(each_answer)
    write_the_file(ANSWER_FILE_PATH, answers, ANSWER_HEADER, append=False, delete=True)

def sort_data(list_of_dicts, order_by, order_direction):
    converted_list = convert_numbers_in_questions_to_int(list_of_dicts)
    sorted_list_of_dicts = sorted(converted_list, key=lambda item: item[order_by], reverse=True if order_direction == 'desc' else False)
    return sorted_list_of_dicts

def convert_numbers_in_questions_to_int(all_questions):
    for i in range(len(all_questions)):
        all_questions[i]['vote_number'] = int(all_questions[i]['vote_number'])
        all_questions[i]['view_number'] = int(all_questions[i]['view_number'])
    return all_questions

def update_question(edited_question):
    write_the_file(QUESTION_FILE_PATH, edited_question, DATA_HEADER, append=False)


def update_answer(edited_answer):
    write_the_file(ANSWER_FILE_PATH, edited_answer, ANSWER_HEADER, append=False)

def allowed_image(filename):
    if not "." in filename:
        return False
    ext = filename.rsplit(".",1)[1]
    if ext.upper() in ALLOWED_IMAGE_TYPE:
        return True
    else:
        return False

# def delete_image_by_question_id():
