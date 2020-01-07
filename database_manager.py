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
