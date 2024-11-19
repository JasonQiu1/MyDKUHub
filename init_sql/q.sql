-- select all the courses taught by one instructor
select 
    c.name as course_name,
    s.year,
    s.term,
    s.session,
    s.type,
    ts.start_time,
    ts.end_time,
    st.day
from instructor i
join teaches t on i.id = t.instructor_id
join section s on t.section_id = s.id
join course c on s.course_id = c.id and s.type = c.type
join section_time st on s.id = st.section_id
join time_slot ts on st.time_slot_id = ts.id
where i.first_name = 'mustafa' and i.last_name = 'misir';


-- all courses that the student with id has already taken
select 
    c.id as course_id,
		c.type as type,
    c.name as course_name,
    c.dept_name,
    c.credits,
    s.term,
    s.session,
    s.year,
    e.grade,
    i.first_name as instructor_first_name,
    i.last_name as instructor_last_name,
    cl.building_name,
    cl.room_name,
    group_concat(distinct concat(st.day, ' ', date_format(ts.start_time, '%H:%i'), '-', date_format(ts.end_time, '%H:%i')) order by ts.start_time separator ', ') as course_schedule
from enrollment e
join section s on e.section_id = s.id
join course c on s.course_id = c.id and s.type = c.type
join teaches t on s.id = t.section_id
join instructor i on t.instructor_id = i.id
join classroom cl on s.building_name = cl.building_name and s.room_name = cl.room_name
join section_time st on s.id = st.section_id
join time_slot ts on st.time_slot_id = ts.id
where e.student_id = 'yg202'
group by e.student_id, c.type, c.id, c.name, c.dept_name, c.credits, s.term, s.session, s.year, e.grade, i.first_name, i.last_name, cl.building_name, cl.room_name
order by s.year desc, s.term, s.session, c.id, c.credits desc;



-- display the student course history (transcript) using procedure 
drop procedure if exists get_passed_courses;
delimiter $$
create procedure get_passed_courses(
    in student_netid varchar(10),
    in start_term varchar(20)
)
begin
    select 
        c.id as course_id,
        c.name as course_name,
        e.grade,
				s.year as year,
        s.term as course_term,
        s.session as course_session
    from enrollment e
    join section s on e.section_id = s.id
    join course c on s.course_id = c.id and s.type = c.type
    where 
        e.student_id = student_netid
        and concat(s.year, ' ', s.term) >= start_term
        and e.grade in ('a', 'b', 'c')
    order by s.year, s.term, s.session, c.id;
end$$
delimiter ;
call get_passed_courses('yg202', '2023 spring');






