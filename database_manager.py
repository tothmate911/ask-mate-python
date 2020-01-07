import database_common
from psycopg2.extensions import AsIs


@database_common.connection_handler
def get_all_questions(cursor):
    cursor.execute("""
                    SELECT * FROM question; 
                   """)
    all_questions = cursor.fetchall()
    return  all_questions

@database_common.connection_handler
def write_new_comment(cursor,to_write_dict):
    columns = to_write_dict.keys()
    values = [to_write_dict[column] for column in columns]

    insert_statement = 'insert into comment (%s) values %s'

    cursor.execute(insert_statement, (AsIs(','.join(columns)), tuple(values)))
