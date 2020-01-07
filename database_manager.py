import database_common

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
    cursor.execute("""
                    INSERT INTO question (submission_time, view_number, vote_number, title, message, image)
                    VALUES (%(s_t)s, %(vi_n)s, %(vo_n)s, %(t)s, %(m)s, %(i)s);
                    """,
                   {'s_t': new_question['submission_time'],
                    'vi_n': new_question['view_number'],
                    'vo_n': new_question['vote_number'],
                    't': new_question['title'],
                    'm': new_question['message'],
                    'i': new_question['image']})
    pass


@database_common.connection_handler
def get_question_by_id(cursor, question_id):
    cursor.execute("""
                    SELECT * FROM question
                    WHERE id = %(question_id)s;
                    """,
                   {'question_id': question_id})
    question = cursor.fetchall()
    print(question)
    return question
