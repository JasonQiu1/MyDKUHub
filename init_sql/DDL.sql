drop table if exists login_info;
drop table if exists balance;
drop table if exists enrollment;
drop table if exists shopping;
drop table if exists phone_number;
drop table if exists address;
drop table if exists credit_limit;
drop table if exists section_time;
drop table if exists teaches;
drop table if exists section;
drop table if exists course_division;
drop table if exists subcourse;
drop table if exists course_req;
drop table if exists course;
drop table if exists advised;
drop table if exists instructor;
drop table if exists dept;
drop table if exists time_slot;
drop table if exists classroom;
drop table if exists building;
drop table if exists hold;
drop table if exists student;
drop table if exists major;
drop table if exists admin;
drop table if exists instructor_deletion_log;
drop table if exists past_instructor;
drop table if exists instructor_master;

create table dept (
    name varchar(50) primary key,
    budget int not null,
    check (budget > 0) 
);

create table building (
    name varchar(100) primary key
);

create table classroom (
    building_name varchar(100) not null,
    room_name varchar(50) not null,
    primary key (building_name, room_name),
    foreign key (building_name) references building(name)
        on delete cascade
        on update cascade
);

create table major(
	name varchar(100) primary key
);

create table student (
    id varchar(10) primary key,
    first_name varchar(100) not null,
    last_name varchar(100) not null,
    major varchar(100) default 'Not Declared',
    class varchar(4),
		foreign key (major) references major(name)
);

create table instructor (
    id varchar(10) primary key,
    first_name varchar(100) not null,
    last_name varchar(100) not null,
    dept varchar(50),
    salary int not null,
    isDuke boolean,
    foreign key (dept) references dept(name)
        on delete set null
        on update cascade,
    check (salary > 0) 
);
create table instructor_master (
    id varchar(10) primary key,
    first_name varchar(100) not null,
    last_name varchar(100) not null,
    dept varchar(50),
    salary int not null,
    isDuke boolean,
    is_active boolean not null
);

create table past_instructor (
    id varchar(10) primary key,
    first_name varchar(100) not null,
    last_name varchar(100) not null,
    dept varchar(50),
    salary int not null,
    isDuke boolean,
    deleted_on datetime not null default current_timestamp
);

create table instructor_deletion_log (
    instructor_id varchar(10),
    deleted_on datetime not null default current_timestamp,
    reason varchar(255),
    primary key (instructor_id)
);

create table advised (
    student_id varchar(10) primary key,
    advisor_id varchar(10),
    foreign key (student_id) references student(id)
        on delete cascade
        on update cascade,
    foreign key (advisor_id) references instructor(id)
        on delete set null
        on update cascade
);

create table course (
    id varchar(50), 
    type enum('lec', 'sem', 'lab', 'rec') not null,
    name varchar(100) not null,
    description text, 
    dept_name varchar(50),  
    credits numeric(2, 1) not null,
    primary key (id, type),
    foreign key (dept_name) references dept(name)
        on delete set null
        on update cascade,
    check (credits >= 0) 
);

create table course_req (
    course_id varchar(50),
    req_id varchar(50),
    type enum('antireq', 'prereq', 'coreq') not null,
    group_id int,
    primary key (course_id, req_id, type, group_id),
    foreign key (course_id) references course(id)
        on delete cascade
        on update cascade,
    foreign key (req_id) references course(id)
        on delete cascade
        on update cascade
);

create table section (
    id int auto_increment primary key,
    course_id varchar(50) not null, 
    type enum('lec', 'sem', 'lab', 'rec') not null,
    term enum('spring', 'fall', 'summer') not null,
    session enum('first', 'second', 'mini', 'semester') not null,
    year int not null,
    capacity int not null,
    building_name varchar(100) not null,
    room_name varchar(50) not null,
    foreign key (course_id, type) references course(id, type)
        on delete cascade
        on update cascade,
    foreign key (building_name, room_name) references classroom(building_name, room_name)
        on delete restrict
        on update cascade 
);



create table teaches (
    instructor_id varchar(10),
    section_id int,
    primary key (instructor_id, section_id),
    foreign key (instructor_id) references instructor_master(id)
				on delete cascade
        on update cascade,
    foreign key (section_id) references section(id)
        on delete cascade
        on update cascade
);

create table time_slot (
    id int auto_increment primary key,
    start_time time not null,
    end_time time not null,
    check (end_time > start_time)
);

create table section_time (
    section_id int not null,
    time_slot_id int not null,
    day enum('mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun') not null,
    primary key (section_id, time_slot_id, day),
    foreign key (section_id) references section(id)
        on delete cascade
        on update cascade,
    foreign key (time_slot_id) references time_slot(id)
        on delete cascade
        on update cascade
);

create table credit_limit (
    student_id varchar(10) not null, 
    year int not null,
    term enum('spring', 'fall', 'summer') not null, 
    session enum('first', 'second', 'mini', 'semester') not null, 
    credit_limit int not null, 
    primary key (student_id, year, term, session),
    foreign key (student_id) references student(id)
        on delete cascade
        on update cascade,
    check (credit_limit > 0) 
);

create table shopping (
    student_id varchar(10),
    section_id int not null,
    primary key (student_id, section_id),
    foreign key (student_id) references student(id)
        on delete cascade
        on update cascade,
    foreign key (section_id) references section(id)
        on delete cascade
        on update cascade
);

create table enrollment (
    student_id varchar(10),
    section_id int,
    grade varchar(5),
    primary key (student_id, section_id),
    foreign key (student_id) references student(id)
        on delete cascade
        on update cascade,
    foreign key (section_id) references section(id)
        on delete cascade
        on update cascade,
	CONSTRAINT check_grade_validity CHECK (grade IN ('A+', 'A', 'A-', 'B+', 'B', 'B-', 'C+', 'C', 'C-', 'D+', 'D', 'D-', 'F', 'NC', 'CR'))
);

create table phone_number (
    id int auto_increment,
    student_id varchar(10),
    type enum('work', 'cell', 'home') not null,
    country_code int not null,
    area_code int not null,
    number varchar(11) not null,
    primary key (id),
    foreign key (student_id) references student(id)
        on delete cascade
        on update cascade
);

create table address (
    id int auto_increment,
    student_id varchar(10),
    type enum('home', 'mail') not null,
    country varchar(100) not null,
    province varchar(100) not null,
    city varchar(100) not null,
    zip_code varchar(20),
    street varchar(100) not null,
    street_number varchar(20) not null,
    unit varchar(20),
    primary key (id),
    foreign key (student_id) references student(id)
        on delete cascade
        on update cascade
);

create table balance (
    student_id varchar(50),
    due int,
    paid int,
    primary key (student_id),
    foreign key (student_id) references student(id)
        on delete cascade
        on update cascade
);

create table admin (
    admin_id varchar(10),
    primary key (admin_id)
);

create table login_info (
    id varchar(10) primary key,
    password varchar(100) not null,
    type enum('student', 'instructor', 'admin') not null
);

create table hold (
		student_id varchar(50),
		type enum('advising', 'registrar') not null,
		primary key (student_id, type),
		foreign key (student_id) references student(id)
        on delete cascade
        on update cascade
);

create table course_division (
    course_id varchar(50) primary key,
    division enum('Art and Humanity', 'Natural Science', 'Social Science') not null,
		foreign key (course_id) references course(id) 
        on delete cascade on update cascade
		
);
