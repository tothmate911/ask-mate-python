import database_common
from psycopg2.extensions import AsIs


@database_common.connection_handler
def get_all_questions_sorted(cursor, order_by='submission_time', order_direction='asc'):
    cursor.execute(f"""
                    SELECT * FROM question
                    ORDER BY {order_by} {order_direction};
                    """)
    all_questions_sorted = cursor.fetchall()
    return all_questions_sorted


@database_common.connection_handler
def get_five_latest_questions_sorted(cursor, order_by='submission_time', order_direction='DESC'):
    cursor.execute(f"""
                    SELECT * FROM
                    (
                        SELECT * FROM question
                        ORDER BY submission_time DESC
                        LIMIT 5
                    ) AS T1 ORDER BY {order_by} {order_direction};
                    """)
    five_latest_questions_sorted = cursor.fetchall()
    return five_latest_questions_sorted


@database_common.connection_handler
def add_question(cursor, new_question):
    cursor.execute("""
                    INSERT INTO question (submission_time, view_number, vote_number, title, message, image)
                    VALUES (%s, %s, %s, %s, %s, %s);
                    """,
                   (new_question['submission_time'],
                    new_question['view_number'],
                    new_question['vote_number'],
                    new_question['title'],
                    new_question['message'],
                    new_question['image']))


@database_common.connection_handler
def add_answer(cursor, new_answer):
    cursor.execute(f"""
                INSERT INTO answer (submission_time, vote_number, question_id, message, image)
                VALUES ('{new_answer['submission_time']}', {new_answer['vote_number']}, {new_answer['question_id']}, '{new_answer['message']}', '{new_answer['image']}');     
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
        SELECT question.id, question.submission_time, question.view_number, question.vote_number, question.title, question.message, question.image 
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
                    SET title = '{updated_question['title']}', message = '{updated_question['message']}'
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
