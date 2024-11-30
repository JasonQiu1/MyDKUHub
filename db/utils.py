def get_enrolled_courses(db_connection, student_id, term=None, session=None, year=None):
    query = """
    SELECT 
        c.id AS course_id,
        c.type AS type,
        c.name AS course_name,
        c.dept_name,
        c.credits,
        s.term,
        s.session,
        s.year,
        s.id AS section_id,
        i.first_name AS instructor_first_name,
        i.last_name AS instructor_last_name
    FROM enrollment e
    JOIN section s ON e.section_id = s.id
    JOIN course c ON s.course_id = c.id AND s.type = c.type
    JOIN teaches t ON s.id = t.section_id
    JOIN instructor i ON t.instructor_id = i.id
    WHERE e.student_id = %s
    """
    params = [student_id]

    # Add optional filters
    if term:
        query += " AND s.term = %s"
        params.append(term)
    if session:
        query += " AND s.session = %s"
        params.append(session)
    if year:
        query += " AND s.year = %s"
        params.append(year)

    query += " ORDER BY s.year DESC, s.term, s.session, c.id, c.credits DESC;"
    return db_connection.execute_query(query, tuple(params))

def get_matching_sections(db_connection, year, term, session, dept_name, instructor_name):
    query = """
    SELECT 
        c.id AS course_id,
        c.name AS course_name,
        c.dept_name,
        c.credits,
        s.id AS section_id,
        s.type AS type,
        s.term,
        s.session,
        s.year,
        s.capacity,
        cl.building_name,
        cl.room_name,
        GROUP_CONCAT(
            DISTINCT CONCAT(i.first_name, ' ', i.last_name)
            ORDER BY i.first_name, i.last_name SEPARATOR '/'
        ) AS instructors,
        GROUP_CONCAT(
            DISTINCT CONCAT(st.day, ' ', DATE_FORMAT(ts.start_time, '%H:%i'), '-', DATE_FORMAT(ts.end_time, '%H:%i'))
            ORDER BY ts.start_time SEPARATOR ', '
        ) AS course_schedule
    FROM section s
    JOIN course c ON s.course_id = c.id AND s.type = c.type
    JOIN teaches t ON s.id = t.section_id
    JOIN instructor i ON t.instructor_id = i.id
    JOIN classroom cl ON s.building_name = cl.building_name AND s.room_name = cl.room_name
    JOIN section_time st ON s.id = st.section_id
    JOIN time_slot ts ON st.time_slot_id = ts.id
    WHERE s.year = %s AND s.term = %s
    """
    params = [year, term]

    if session:
        query += " AND s.session = %s"
        params.append(session)

    if dept_name:
        query += " AND c.dept_name = %s"
        params.append(dept_name)

    if instructor_name:
        query += """
        AND s.id IN (
            SELECT s_inner.id
            FROM section s_inner
            JOIN teaches t_inner ON s_inner.id = t_inner.section_id
            JOIN instructor i_inner ON t_inner.instructor_id = i_inner.id
            WHERE CONCAT(i_inner.first_name, ' ', i_inner.last_name) LIKE %s
        )
        """
        params.append(f"%{instructor_name}%")

    query += """
    GROUP BY 
        c.id, c.name, c.dept_name, c.credits, 
        s.id, s.type, s.term, s.session, s.year, s.capacity, 
        cl.building_name, cl.room_name
    ORDER BY s.year DESC, s.term, s.session, c.id, c.credits DESC;
    """

    return db_connection.execute_query(query, tuple(params))
