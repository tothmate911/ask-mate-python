import database_common

@database_common.connection_handler
def get_all_questions(cursor):
    cursor.execute("""
                    SELECT * FROM question; 
                   """)
    all_questions = cursor.fetchall()
    return  all_questions

@database_common.connection_handler
def write_new_comment(cursor,to_write_dict):
    placeholders = ', '.join(['%s'] * len(to_write_dict))
    columns = ', '.join(to_write_dict.keys())
    sql = "INSERT INTO %s ( %s ) VALUES ( %s )" % ('comment', columns, placeholders)
    cursor.execute(sql, to_write_dict.values())