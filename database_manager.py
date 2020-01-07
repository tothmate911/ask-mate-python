import database_common
from datetime import datetime

@database_common.connection_handler
def get_all_questions_sorted(cursor, order_by, order_direction):
    cursor.execute("""
                    SELECT * FROM question
                    ORDER BY %s %s;
                   """ %
                ("".join(order_by), "".join(order_direction)))
    all_questions_sorted = cursor.fetchall()
    return all_questions_sorted

@database_common.connection_handler
def add_question(cursor, new_question):
    dt = datetime.now()
    cursor.execute("""
                    SELECT * FROM question; 
                   """)
    all_questions = cursor.fetchall()
    return  all_questions

@database_common.connection_handler
def search_in_questions(cursor, search_phrase):
    cursor.execute(F"""
        SELECT question.id, question.submission_time, question.view_number, question.vote_number, question.title, question.message, question.image 
        FROM question 
        FULL JOIN answer a on question.id = a.question_id
        WHERE question.title LIKE '%{search_phrase}%'
        OR question.message LIKE '%{search_phrase}%'
        OR a.message LIKE '%{search_phrase}%'
    """)
    searched_question = cursor.fetchall()
    return searched_question

@database_common.connection_handler
def search_in_answers(cursor, search_phrase):
    cursor.execute(F"""
        SELECT * 
        FROM answer 
        WHERE message LIKE '%{search_phrase}%'
    """)
    searched_answer = cursor.fetchall()
    return searched_answer
                    INSERT INTO question (submission_time, view_number, vote_number, title, message, image)
                    VALUES (%(s_t)s, %(vi_n)s, %(vo_n)s, %(t)s, %(m)s, %(i)s);
                    """,
                   {'s_t': dt,
                    'vi_n': new_question['view_number'],
                    'vo_n': new_question['vote_number'],
                    't': new_question['title'],
                    'm': new_question['message'],
                    'i': new_question['image']})
    pass
