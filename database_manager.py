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

