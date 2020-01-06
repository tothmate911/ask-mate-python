import database_common

@database_common.connection_handler
def get_all_questions(cursor):
    cursor.execute("""
                    SELECT * FROM question; 
                   """)
    all_questions = cursor.fetchall()
    return  all_questions