import os
import database_manager

ANSWER_FILE_PATH = 'sample_data/answer.csv'
QUESTION_FILE_PATH = 'sample_data/question.csv'
IMAGE_UPLOAD_PATH = "static/images"
ALLOWED_IMAGE_TYPE = ["PNG", "JPG"]
ROOT_PATH = 'static/images'


def sort_data(list_of_dicts, order_by, order_direction):
    converted_list = convert_numbers_in_list_to_int(list_of_dicts)
    sorted_list_of_dicts = sorted(converted_list, key=lambda item: item[order_by],
                                  reverse=True if order_direction == 'desc' else False)
    return sorted_list_of_dicts


def convert_numbers_in_list_to_int(all_data):
    for i in range(len(all_data)):
        all_data[i]['vote_number'] = int(all_data[i]['vote_number'])
        try:
            all_data[i]['view_number'] = int(all_data[i]['view_number'])
        except KeyError:
            continue
    return all_data


def allowed_image(filename):
    if not "." in filename:
        return False
    ext = filename.rsplit(".", 1)[1]
    if ext.upper() in ALLOWED_IMAGE_TYPE:
        return True
    else:
        return False


def get_image_path_for_question_by_id(question_id):
    delete_file = []
    question = database_manager.get_question_by_id(question_id)
    answers_by_question = database_manager.get_all_answer_by_question_id_sorted(question_id)
    delete_file.append(question[0]['image'])
    for answer in answers_by_question:
        delete_file.append(answer['image'])
    return delete_file


def get_image_path_for_answer_by_id(answer_id):
    answer = database_manager.get_answer_by_id(answer_id)
    return answer[0]['image']


def delete_image_by_id(id, answer=False):
    try:
        if answer:
            path = get_image_path_for_answer_by_id(id)
            os.remove(path)
        else:
            path = get_image_path_for_question_by_id(id)
            for file in path:
                os.remove(file)
    except:
        pass


def apostroph_change(text):
    change = ('title', 'message', 'name')
    new_text = text
    for column in change:
        try:
            new_text[column] = text[column].replace('\'', '\"')
        except:
            continue
    return new_text

def search_highlight(text, search_word):
    change = ('title', 'message', 'name')
    new_text = text
    for element_index in range(len(text)):
        for column in change:
            try:
                new_text[element_index][column] = text[element_index][column].replace(f'{search_word}', f'<b>{search_word}</b>')
            except:
                continue
    return new_text

def remove_from_list(questions):
    remove = []
    for index in range(len(questions)):
        if questions[index]['id'] is None:
            remove.append(questions[index])
    for element in remove:
        questions.remove(element)
    return questions

def tag_duplicate_check(tag):
    all_tag = database_manager.all_tag_name()
    for element in all_tag:
        if element['name'] == tag:
            return True
    return False