CREATE OR REPLACE VIEW matching_sections_view AS
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
JOIN instructor_master i ON t.instructor_id = i.id
JOIN classroom cl ON s.building_name = cl.building_name AND s.room_name = cl.room_name
JOIN section_time st ON s.id = st.section_id
JOIN time_slot ts ON st.time_slot_id = ts.id
GROUP BY 
    c.id, c.name, c.dept_name, c.credits, 
    s.id, s.type, s.term, s.session, s.year, s.capacity, 
    cl.building_name, cl.room_name
ORDER BY s.year DESC, s.term, s.session, c.id, c.credits DESC;


CREATE OR REPLACE VIEW enrolled_courses_view AS
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
    i.last_name AS instructor_last_name,
    e.student_id
FROM enrollment e
JOIN section s ON e.section_id = s.id
JOIN course c ON s.course_id = c.id AND s.type = c.type
JOIN teaches t ON s.id = t.section_id
JOIN instructor_master i ON t.instructor_id = i.id
ORDER BY s.year DESC, s.term, s.session, c.id, c.credits DESC;
