import database_common
from datetime import datetime
from psycopg2 import sql
from psycopg2.extensions import AsIs


@database_common.connection_handler
def get_all_questions_sorted_with_reputation(cursor, order_by='submission_time', order_direction='asc'):
    cursor.execute(f"""
                    SELECT * 
                    FROM question JOIN users
                    ON question.username = users.user_name
                    ORDER BY {order_by} {order_direction};
                    """)
    all_questions_sorted = cursor.fetchall()
    return all_questions_sorted


@database_common.connection_handler
def get_five_latest_questions_sorted_with_reputation(cursor, order_by='submission_time', order_direction='DESC'):
    cursor.execute(f"""
                    SELECT * FROM
                    (
                        SELECT *
                        FROM question JOIN users
                        ON question.username = users.user_name
                        ORDER BY submission_time DESC
                        LIMIT 5
                    ) AS T1 ORDER BY {order_by} {order_direction};
                    """)
    five_latest_questions_sorted = cursor.fetchall()
    return five_latest_questions_sorted


@database_common.connection_handler
def add_question(cursor, new_question):
    cursor.execute("""
                    INSERT INTO question (submission_time, view_number, vote_number, title, message, image, username)
                    VALUES (%s, %s, %s, %s, %s, %s, %s);
                    """,
                   (new_question['submission_time'],
                    new_question['view_number'],
                    new_question['vote_number'],
                    new_question['title'],
                    new_question['message'],
                    new_question['image'],
                    new_question['username']
                    ))


@database_common.connection_handler
def add_answer(cursor, new_answer):
    cursor.execute(f"""
                INSERT INTO answer (submission_time, vote_number, question_id, message, image,username)
                VALUES ('{new_answer['submission_time']}', {new_answer['vote_number']}, {new_answer['question_id']}, '{new_answer['message']}', '{new_answer['image']}', '{new_answer['username']}');     
    """)


@database_common.connection_handler
def get_question_by_id(cursor, question_id):
    cursor.execute(f"""
                    SELECT * FROM question
                    WHERE id = {question_id};
                    """)
    question = cursor.fetchall()
    return question


@database_common.connection_handler
def get_all_comment_from_question_id(cursor, question_id):
    cursor.execute(f"""
                    SELECT * FROM comment
                    WHERE question_id={question_id} AND answer_id is null;""")
    question_comment = cursor.fetchall()
    return question_comment


@database_common.connection_handler
def get_all_comment_from_answer_id(cursor, question_id):
    cursor.execute(f"""
                    SELECT * FROM comment
                    WHERE question_id={question_id} and answer_id is not null;""")
    answer_comment = cursor.fetchall()
    return answer_comment


@database_common.connection_handler
def get_answer_by_id(cursor, answer_id):
    cursor.execute(f"""
                    SELECT * FROM answer
                    WHERE id = {answer_id};
                    """)
    answer = cursor.fetchall()
    return answer


@database_common.connection_handler
def get_comment_by_id(cursor, comment_id):
    cursor.execute(f"""
                    SELECT * FROM comment
                    WHERE id = {comment_id};
                    """)
    comment = cursor.fetchall()
    return comment


@database_common.connection_handler
def get_all_answer_by_question_id_sorted(cursor, question_id, order_by='submission_time', order_direction='asc'):
    cursor.execute(f"""
                    SELECT * FROM answer
                    WHERE question_id={question_id}
                    ORDER BY {order_by} {order_direction}
                    """)
    answers = cursor.fetchall()
    return answers


@database_common.connection_handler
def delete_question(cursor, question_id):
    delete_tag_by_question_id(question_id)
    cursor.execute(f"""
                    DELETE FROM comment
                    WHERE question_id = {question_id}""")
    cursor.execute(f"""
                    DELETE FROM answer
                    WHERE question_id = {question_id};""")
    cursor.execute(f"""
                    DELETE FROM question
                    WHERE id = {question_id};""")


@database_common.connection_handler
def delete_answer(cursor, answer_id):
    cursor.execute(f"""
                    DELETE FROM comment
                    WHERE answer_id = {answer_id}""")
    cursor.execute(f"""
                    DELETE FROM answer
                    WHERE id = {answer_id}""")


@database_common.connection_handler
def delete_comment(cursor, comment_id):
    cursor.execute(f"""
                    DELETE FROM comment
                    WHERE id = {comment_id}""")


@database_common.connection_handler
def search_in_questions(cursor, search_phrase):
    cursor.execute(F"""
        SELECT DISTINCT (question.id), question.submission_time, question.view_number, question.vote_number, question.title, question.message, question.image 
        FROM question 
        FULL JOIN answer a on question.id = a.question_id
        FULL JOIN question_tag qt on question.id = qt.question_id
        FULL JOIN tag t on qt.tag_id = t.id
        WHERE question.title LIKE '%{search_phrase}%'
        OR question.message LIKE '%{search_phrase}%'
        OR a.message LIKE '%{search_phrase}%'
        OR t.name LIKE '%{search_phrase}%';
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


@database_common.connection_handler
def write_new_comment(cursor, to_write_dict):
    columns = to_write_dict.keys()
    values = [to_write_dict[column] for column in columns]

    insert_statement = 'insert into comment (%s) values %s'

    cursor.execute(insert_statement, (AsIs(','.join(columns)), tuple(values)))


@database_common.connection_handler
def vote(cursor, id, type, vote):
    cursor.execute(f"""
                    UPDATE {type}
                    SET vote_number = vote_number {vote} 1
                    WHERE id = {id}
                    """)


@database_common.connection_handler
def update_question(cursor, updated_question):
    cursor.execute(f"""
                    UPDATE question
                    SET title = '{updated_question['title']}', message = '{updated_question['message']}', accepted_answer_id = {updated_question['accepted_answer_id']}
                    WHERE id = {updated_question['id']}""")


@database_common.connection_handler
def view_up(cursor, id):
    cursor.execute(f"""
                    UPDATE question
                    SET view_number = view_number + 1
                    WHERE id = {id}""")


@database_common.connection_handler
def update_answer(cursor, answer, id):
    cursor.execute(f"""
                    UPDATE answer
                    SET message = '{answer['message']}'
                    WHERE id = {id}""")


@database_common.connection_handler
def update_comment(cursor, comment, id):
    cursor.execute(f"""
                    UPDATE comment
                    SET message = '{comment['message']}', edited_count=edited_count+1, submission_time='{comment['submission_time']}'
                    WHERE id = {id}""")


@database_common.connection_handler
def all_tag_name(cursor):
    cursor.execute("""
                    SELECT * FROM tag
    """)
    tags = cursor.fetchall()
    return tags


@database_common.connection_handler
def tag_id_by_tag_name(cursor, tag):
    cursor.execute(f"""
                    SELECT * FROM tag
                    WHERE name = '{tag}'
    """)
    tag = cursor.fetchall()
    return tag


@database_common.connection_handler
def add_tag(cursor, tag, question_id):
    cursor.execute(f"""
                    INSERT INTO tag (name)
                    VALUES ('{tag['name']}');
    """)
    tag_id = tag_id_by_tag_name(tag['name'])[0]
    cursor.execute(f"""
                    INSERT INTO question_tag (question_id, tag_id)
                    VALUES ({question_id}, {tag_id['id']});
    """)

@database_common.connection_handler
def add_old_tag(cursor, tag, question_id):
    tag_id = tag_id_by_tag_name(tag['name'])[0]
    cursor.execute(f"""
                    INSERT INTO question_tag (question_id, tag_id)
                    VALUES ({question_id}, {tag_id['id']});
    """)


@database_common.connection_handler
def delete_tag_by_question_id(cursor, question_id):
    cursor.execute(f"""
                    DELETE FROM question_tag
                    WHERE question_id = {question_id}
    """)


@database_common.connection_handler
def delete_tag(cursor, tag_id, question_id):
    cursor.execute(f"""
                    DELETE FROM question_tag
                    WHERE tag_id = {tag_id} AND question_id = {question_id}
    """)


@database_common.connection_handler
def all_question_by_tag_id(cursor, tag_id):
    cursor.execute(f"""
                    SELECT question.id, question.submission_time, question.view_number, question.vote_number, question.title, question.message, question.image
                    FROM question
                    FULL JOIN question_tag qt on question.id = qt.question_id
                    WHERE qt.tag_id = {tag_id}
    """)
    questions = cursor.fetchall()
    return questions


@database_common.connection_handler
def tag_by_tag_id(cursor, tag_id):
    cursor.execute(f"""
                    SELECT * FROM tag
                    WHERE id = {tag_id}
    """)
    tag = cursor.fetchall()
    return tag


@database_common.connection_handler
def all_tag(cursor):
    cursor.execute(f"""
                    SELECT * FROM question_tag
                    FULL JOIN tag t on question_tag.tag_id = t.id
                    WHERE question_tag.question_id IS NOT null;
    """)
    tags = cursor.fetchall()
    return tags

@database_common.connection_handler
def member_registration(cursor, username,hashed_pw):
    cursor.execute(f"""
                    INSERT INTO users(user_name, hash_password, date)
                    VALUES (%s,%s,%s)""",
                   (username,hashed_pw,datetime.now()))

@database_common.connection_handler
def get_hashed_pw_for_username(cursor, username):
    cursor.execute("""
                    SELECT hash_password FROM users
                    WHERE user_name = %(user_name)s
                    """, {'user_name': username})
    hashed_pw_for_username = cursor.fetchone().get('hash_password', None)
    return hashed_pw_for_username

@database_common.connection_handler
def all_user(cursor):
    cursor.execute("""
                    SELECT user_name, reputation FROM users
                    ORDER BY user_name;
    """)
    return cursor.fetchall()

@database_common.connection_handler
def question_of_user(cursor, user_name):
    cursor.execute("""
                    SELECT DISTINCT(question.id), question.submission_time, question.view_number, question.vote_number, question.title, question.message, question.image, question.username FROM question
                    FULL JOIN answer a on question.id = a.question_id
                    FULL JOIN comment c on question.id = c.question_id 
                    WHERE question.username = %(user_name)s
                    OR a.username = %(user_name)s
                    OR c.username = %(user_name)s
    """, {'user_name': user_name})
    return cursor.fetchall()

@database_common.connection_handler
def answer_of_user(cursor, user_name):
    cursor.execute("""
                    SELECT DISTINCT (answer.id), answer.id, answer.submission_time, answer.vote_number, answer.question_id, answer.message, answer.image, answer.username FROM answer
                    FULL JOIN comment c on answer.id = c.answer_id
                    WHERE answer.username = %(user_name)s
                    OR c.username = %(user_name)s
    """, {'user_name': user_name})
    return cursor.fetchall()

@database_common.connection_handler
def comment_of_user(cursor, user_name):
    cursor.execute("""
                    SELECT * FROM comment
                    WHERE username = %(user_name)s
    """, {'user_name': user_name})
    return cursor.fetchall()


@database_common.connection_handler
def check_if_user_voted_for_question(cursor, user, question_id):
    cursor.execute("""
                    SELECT
                    CASE WHEN EXISTS (SELECT vote_value FROM votes
                                      WHERE user_name = %(user_name)s AND question_id = %(question_id)s)
                         THEN 'True'
                         ELSE 'False'
                    END AS exist
                    """, {'user_name': user, 'question_id': question_id})
    if cursor.fetchone()['exist'] == 'True':
        return True
    else:
        return False


@database_common.connection_handler
def get_user_vote_for_question(cursor, user, question_id):
    if check_if_user_voted_for_question(user, question_id) is True:
        cursor.execute("""
                        SELECT vote_value FROM votes
                        WHERE user_name = %(user_name)s AND question_id = %(question_id)s;
                        """, {'user_name': user, 'question_id': question_id})
        user_vote_for_question = cursor.fetchone()['vote_value']
    else:
        user_vote_for_question = None
    return user_vote_for_question


@database_common.connection_handler
def add_user_vote_for_question(cursor, user, question_id, vote_value):
    cursor.execute("""
                    INSERT INTO votes
                    (user_name, question_id, vote_value)
                    VALUES (%(user_name)s, %(question_id)s, %(vote_value)s)
                    """, {'user_name': user, 'question_id': question_id, 'vote_value': vote_value})


@database_common.connection_handler
def update_user_vote_for_question(cursor, user, question_id, vote_value):
    cursor.execute("""
                    UPDATE votes
                    SET vote_value = %(vote_value)s
                    WHERE user_name = %(user_name)s and question_id = %(question_id)s
                    """, {'user_name': user, 'question_id': question_id, 'vote_value': vote_value})









@database_common.connection_handler
def check_if_user_voted_for_answer(cursor, user, answer_id):
    cursor.execute("""
                    SELECT
                    CASE WHEN EXISTS (SELECT vote_value FROM votes
                                      WHERE user_name = %(user_name)s AND answer_id = %(answer_id)s)
                         THEN 'True'
                         ELSE 'False'
                    END AS exist
                    """, {'user_name': user, 'answer_id': answer_id})
    if cursor.fetchone()['exist'] == 'True':
        return True
    else:
        return False


@database_common.connection_handler
def get_user_vote_for_answer(cursor, user, answer_id):
    if check_if_user_voted_for_answer(user, answer_id) is True:
        cursor.execute("""
                        SELECT vote_value FROM votes
                        WHERE user_name = %(user_name)s AND answer_id = %(answer_id)s;
                        """, {'user_name': user, 'answer_id': answer_id})
        user_vote_for_answer = cursor.fetchone()['vote_value']
    else:
        user_vote_for_answer = None
    return user_vote_for_answer


@database_common.connection_handler
def add_user_vote_for_answer(cursor, user, answer_id, vote_value):
    cursor.execute("""
                    INSERT INTO votes
                    (user_name, answer_id, vote_value)
                    VALUES (%(user_name)s, %(answer_id)s, %(vote_value)s)
                    """, {'user_name': user, 'answer_id': answer_id, 'vote_value': vote_value})


@database_common.connection_handler
def update_user_vote_for_answer(cursor, user, answer_id, vote_value):
    cursor.execute("""
                    UPDATE votes
                    SET vote_value = %(vote_value)s
                    WHERE user_name = %(user_name)s and answer_id = %(answer_id)s
                    """, {'user_name': user, 'answer_id': answer_id, 'vote_value': vote_value})


def update_reputation():

    return None