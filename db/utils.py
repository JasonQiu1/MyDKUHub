def get_enrolled_courses(db_connection, student_id, term=None, session=None, year=None):
    params = [student_id]
    if term:
        query += " AND term = %s"
        params.append(term)
    if session:
        query += " AND session = %s"
        params.append(session)
    if year:
        query += " AND year = %s"
        params.append(year)

    return db_connection.execute_query(query, tuple(params))


def get_matching_sections(db_connection, year, term, session=None, dept_name=None, instructor_name=None):
    query = """
    SELECT * 
    FROM matching_sections_view
    WHERE year = %s AND term = %s
    """
    params = [year, term]

    if session:
        query += " AND session = %s"
        params.append(session)

    if dept_name:
        query += " AND dept_name = %s"
        params.append(dept_name)

    if instructor_name:
        query += " AND instructors LIKE %s"
        params.append(f"%{instructor_name}%")

    return db_connection.execute_query(query, tuple(params))

