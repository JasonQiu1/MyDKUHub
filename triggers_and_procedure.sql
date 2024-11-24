
DROP trigger IF EXISTS check_login_info_before_insert;
delimiter $$
create trigger check_login_info_before_insert
before insert on login_info
for each row
begin
    if new.type = 'student' then
        if not exists (select 1 from student where id = new.id) then
            signal sqlstate '45000'
            set message_text = 'id does not exist in student table for type student';
        end if;
    elseif new.type = 'instructor' then
        if not exists (select 1 from instructor where id = new.id) then
            signal sqlstate '45000'
            set message_text = 'id does not exist in instructor table for type instructor';
        end if;
    elseif new.type = 'admin' then
        if not exists (select 1 from admin where admin_id = new.id) then
            signal sqlstate '45000'
            set message_text = 'id does not exist in admin table for type admin';
        end if;
    end if;
end$$
delimiter ;

DROP PROCEDURE IF EXISTS GenerateUnionQuery;
DELIMITER //
CREATE PROCEDURE GenerateUnionQuery(IN id_list TEXT)
BEGIN
    DECLARE finished INT DEFAULT 0;
    DECLARE id_value INT;
    DECLARE cur CURSOR FOR SELECT id FROM JSON_TABLE(id_list, "$[*]" COLUMNS (id INT PATH "$")) AS jt;
    DECLARE CONTINUE HANDLER FOR NOT FOUND SET finished = 1;
    SET @formatted_id_list = CONCAT('(', REPLACE(REPLACE(id_list, '[', ''), ']', ''), ')');

    -- Initialize the dynamic query
    SET @query = '';

    -- Open the cursor
    OPEN cur;

    read_loop: LOOP
        FETCH cur INTO id_value;
        IF finished THEN 
            LEAVE read_loop;
        END IF;

        -- Append the SELECT statement for the current ID to the query
        SET @query = CONCAT(@query, 
            IF(@query = '', '', ' UNION '), 
            'SELECT DISTINCT s.id AS section_id, 
                    s.type AS section_type, 
                    c.id AS course_id,
                    s.term,
                    s.session,
                    s.year
             FROM section s
             INNER JOIN course c ON s.course_id = c.id AND s.type = c.type
             INNER JOIN teaches t ON s.id = t.section_id
             INNER JOIN instructor i ON t.instructor_id = i.id
             INNER JOIN classroom cl ON s.building_name = cl.building_name AND s.room_name = cl.room_name
             INNER JOIN section_time st ON s.id = st.section_id
             INNER JOIN time_slot ts ON st.time_slot_id = ts.id
             WHERE c.id IN (
                 SELECT s1.course_id 
                 FROM section s1 
                 WHERE s1.id = ', id_value, ')  
             AND s.term IN (
                 SELECT s1.term 
                 FROM section s1 
                 WHERE s1.id = ', id_value, ')
             AND s.session IN (
                 SELECT s1.session 
                 FROM section s1 
                 WHERE s1.id = ', id_value, ')
             AND s.year IN (
                 SELECT s1.year 
                 FROM section s1 
                 WHERE s1.id = ', id_value, ')'
        );
    END LOOP;

    -- Close the cursor
    CLOSE cur;

    -- Use the generated query in a CTE for TempSectionTable
    SET @cte_section = CONCAT(
        'WITH TempSectionTable AS (', @query, '),
        TempValidTable AS (
            SELECT course_id,
                   term,
                   session,
                   year
            FROM (
                SELECT 
                    course_id,
                    term,
                    session,
                    year,
                    GROUP_CONCAT(DISTINCT section_type ORDER BY section_type) AS required_types,
                    GROUP_CONCAT(DISTINCT CASE WHEN section_id IN ', @formatted_id_list, ' THEN section_type ELSE NULL END ORDER BY section_type) AS selected_types,
                    CASE 
                        WHEN GROUP_CONCAT(DISTINCT section_type ORDER BY section_type) = GROUP_CONCAT(DISTINCT CASE WHEN section_id IN ', @formatted_id_list, ' THEN section_type ELSE NULL END ORDER BY section_type)
                        AND COUNT(CASE WHEN section_id IN ', @formatted_id_list, ' THEN section_type END) = COUNT(DISTINCT CASE WHEN section_id IN ', @formatted_id_list, ' THEN section_type END)
                        THEN ''VALID''
                        ELSE ''INVALID''
                    END AS coverage_status
                FROM TempSectionTable
                GROUP BY course_id, term, session, year
            ) AS validation_result
            WHERE coverage_status = ''INVALID''
        )
        SELECT COUNT(*) INTO @group_count FROM TempValidTable;'
    );

    -- Execute the CTE query
    PREPARE stmt_cte FROM @cte_section;
    EXECUTE stmt_cte;
    DEALLOCATE PREPARE stmt_cte;

    -- Handle validation results
    IF @group_count > 0 THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Not all sub_lectures are selected';
    END IF;
END //
DELIMITER ;


DROP PROCEDURE IF EXISTS CheckPrereqsMet;
DELIMITER $$

CREATE PROCEDURE CheckPrereqsMet(
    IN student_id VARCHAR(50),
    IN selected_sections TEXT
)
BEGIN
    DECLARE unmet_groups INT;
    DECLARE error_message VARCHAR(255);
    DECLARE current_course_id VARCHAR(50);
    DECLARE current_year INT;
    DECLARE current_term INT;
    DECLARE current_session INT;
    DECLARE section_id VARCHAR(50);
    DECLARE section_list TEXT;
    DECLARE pos INT;
    DECLARE finished INT DEFAULT 0;
    DECLARE has_prereqs INT;

    -- Initialize section list
    SET section_list = selected_sections;

    -- Label the loop for ITERATE to reference
    section_loop: WHILE NOT finished DO
        -- Extract the next section ID
        SET pos = LOCATE(',', section_list);
        IF pos > 0 THEN
            SET section_id = SUBSTRING(section_list, 1, pos - 1);
            SET section_list = SUBSTRING(section_list, pos + 1);
        ELSE
            SET section_id = section_list;
            SET finished = 1;
        END IF;

        -- Fetch the course_id and schedule details for the current section
        SELECT course_id, year, term, session
        INTO current_course_id, current_year, current_term, current_session
        FROM section
        WHERE id = section_id;

        -- Check if the current course has any prerequisites
        SELECT COUNT(*) INTO has_prereqs
        FROM course_req
        WHERE course_id = current_course_id
          AND type = 'prereq';

        -- If no prerequisites, continue to the next iteration
        IF has_prereqs = 0 THEN
            ITERATE section_loop; -- Skip the rest of the loop and continue
        END IF;

        -- Check if there are any unmet prerequisite groups
        SELECT COUNT(*)
        INTO unmet_groups
        FROM (
            SELECT 
                cr.group_id,
                COUNT(cr.req_id) - SUM(
                    CASE 
                        WHEN e.course_id IS NOT NULL THEN 1
                        ELSE 0
                    END
                ) AS unmet_reqs
            FROM course_req cr
            LEFT JOIN (
                SELECT DISTINCT s.course_id
                FROM enrollment e
                JOIN section s ON e.section_id = s.id
                WHERE e.student_id = student_id
                  AND (s.year < current_year OR
                       (s.year = current_year AND s.term < current_term) OR
                       (s.year = current_year AND s.term = current_term AND s.session < current_session))
            
                UNION
                
                SELECT DISTINCT course_id
                FROM section
                WHERE FIND_IN_SET(id, selected_sections) > 0
                  AND (year < current_year OR
                       (year = current_year AND term < current_term) OR
                       (year = current_year AND term = current_term AND session < current_session))
            
            ) e ON cr.req_id = e.course_id
            WHERE cr.course_id = current_course_id
              AND cr.type = 'prereq'
            GROUP BY cr.group_id
            HAVING unmet_reqs = 0
        ) AS satisfied_groups;

        -- Raise an error if no groups are satisfied
        IF unmet_groups = 0 THEN
            SET error_message = CONCAT('No prerequisites met for course: ', current_course_id);
            SIGNAL SQLSTATE '45000'
                SET MESSAGE_TEXT = error_message;
        END IF;
    END WHILE section_loop;
END$$

DELIMITER ;

DROP PROCEDURE IF EXISTS CheckCoreqsMet;
DELIMITER $$

CREATE PROCEDURE CheckCoreqsMet(
    IN student_id VARCHAR(50),
    IN selected_sections TEXT
)
BEGIN
    DECLARE unmet_groups INT;
    DECLARE error_message VARCHAR(255);
    DECLARE current_course_id VARCHAR(50);
    DECLARE current_year INT;
    DECLARE current_term INT;
    DECLARE current_session INT;
    DECLARE section_id VARCHAR(50);
    DECLARE section_list TEXT;
    DECLARE pos INT;
    DECLARE finished INT DEFAULT 0;
    DECLARE has_coreqs INT;

    -- Initialize section list
    SET section_list = selected_sections;

    -- Label the loop for ITERATE to reference
    section_loop: WHILE NOT finished DO
        -- Extract the next section ID
        SET pos = LOCATE(',', section_list);
        IF pos > 0 THEN
            SET section_id = SUBSTRING(section_list, 1, pos - 1);
            SET section_list = SUBSTRING(section_list, pos + 1);
        ELSE
            SET section_id = section_list;
            SET finished = 1;
        END IF;

        -- Fetch the course_id and schedule details for the current section
        SELECT course_id, year, term, session
        INTO current_course_id, current_year, current_term, current_session
        FROM section
        WHERE id = section_id;

        -- Check if the current course has any co-requisites
        SELECT COUNT(*) INTO has_coreqs
        FROM course_req
        WHERE course_id = current_course_id
          AND type = 'coreq';

        -- If no co-requisites, continue to the next iteration
        IF has_coreqs = 0 THEN
            ITERATE section_loop; -- Skip the rest of the loop and continue
        END IF;

        -- Check if there are any unmet co-requisite groups
        SELECT COUNT(*)
        INTO unmet_groups
        FROM (
            SELECT 
                cr.group_id,
                COUNT(cr.req_id) - SUM(
                    CASE 
                        WHEN e.course_id IS NOT NULL THEN 1
                        ELSE 0
                    END
                ) AS unmet_reqs
            FROM course_req cr
            LEFT JOIN (
                SELECT DISTINCT s.course_id
                FROM enrollment e
                JOIN section s ON e.section_id = s.id
                WHERE e.student_id = student_id
                  AND (s.year <= current_year AND
                       (s.year < current_year OR
                       (s.term <= current_term AND
                       (s.term < current_term OR
                       (s.session <= current_session)))))
                
                UNION
                
                SELECT DISTINCT course_id
                FROM section
                WHERE FIND_IN_SET(id, selected_sections) > 0
                  AND (year <= current_year AND
                       (year < current_year OR
                       (term <= current_term AND
                       (term < current_term OR
                       (session <= current_session))))) -- Apply co-requisite constraints to selected sections
            ) e ON cr.req_id = e.course_id
            WHERE cr.course_id = current_course_id
              AND cr.type = 'coreq'
            GROUP BY cr.group_id
            HAVING unmet_reqs = 0
        ) AS satisfied_groups;

        -- Raise an error if no groups are satisfied
        IF unmet_groups = 0 THEN
            SET error_message = CONCAT('No co-requisites met for course: ', current_course_id);
            SIGNAL SQLSTATE '45000'
                SET MESSAGE_TEXT = error_message;
        END IF;
    END WHILE section_loop;
END$$

DELIMITER ;

DROP PROCEDURE IF EXISTS enroll_selected_courses;

DELIMITER $$
CREATE PROCEDURE enroll_selected_courses(
    student_id VARCHAR(50),
    selected_sections TEXT -- Comma-separated list of section IDs
)
BEGIN
    DECLARE conflict_count INT;
    DECLARE anti_req_violations INT;
    DECLARE credit_exceeded_count INT;
    DECLARE balance_due double;
    DECLARE hold_count BOOLEAN;
    DECLARE over_capacity_count INT;
    DECLARE duplicate_course_count INT;
	DECLARE json_selected_sections TEXT;

    
	SET json_selected_sections = CONCAT('[', selected_sections, ']');

	CALL GenerateUnionQuery(json_selected_sections);
    
    -- check if there is any outstanding payment
    SELECT due - paid INTO balance_due
    FROM balance
    WHERE student_id = student_id;
    IF balance_due > 0 THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Student has outstanding balance';
    END IF;
    

    -- check if there is any hold
	SELECT COUNT(*) INTO hold_count
    FROM hold
    WHERE student_id = student_id
      AND type IN ('advising', 'register');
    IF hold_count > 0 THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Student account is on hold for advising or registration';
    END IF;

    
    -- check if the student already taken the same course before
    SET duplicate_course_count = (
        SELECT COUNT(*)
        FROM enrollment e
        JOIN section s_enrolled ON e.section_id = s_enrolled.id
        JOIN section s_selected ON FIND_IN_SET(s_selected.id, selected_sections)
        WHERE e.student_id = student_id
          AND s_enrolled.course_id = s_selected.course_id
    );
    IF duplicate_course_count > 0 THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Student has already taken one or more of the selected courses';
    END IF;


    -- Check time conflict, with the previous enrollment and the current intended enrollments
    SET conflict_count = (
        SELECT COUNT(*)
        FROM (
            SELECT st1.section_id AS section1, st2.section_id AS section2
            FROM section_time st1
            JOIN time_slot ts1 ON st1.time_slot_id = ts1.id
            JOIN section_time st2 ON st1.section_id <> st2.section_id
            JOIN time_slot ts2 ON st2.time_slot_id = ts2.id
            JOIN section sec1 ON st1.section_id = sec1.id
            JOIN section sec2 ON st2.section_id = sec2.id
            WHERE FIND_IN_SET(st1.section_id, selected_sections)
              AND FIND_IN_SET(st2.section_id, selected_sections)
              AND st1.day = st2.day
              AND ts1.start_time < ts2.end_time
              AND ts1.end_time > ts2.start_time
              AND sec1.term = sec2.term
              AND sec1.session = sec2.session
              AND sec1.year = sec2.year
        ) AS conflicts
    );
    IF conflict_count > 0 THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Time conflict detected within the selected courses';
    END IF;
    SET conflict_count = (
        SELECT COUNT(*)
        FROM section_time st1
        JOIN time_slot ts1 ON st1.time_slot_id = ts1.id
        JOIN enrollment e ON e.student_id = student_id
        JOIN section_time st2 ON e.section_id = st2.section_id
        JOIN time_slot ts2 ON st2.time_slot_id = ts2.id
        JOIN section sec1 ON st1.section_id = sec1.id
        JOIN section sec2 ON e.section_id = sec2.id
        WHERE FIND_IN_SET(st1.section_id, selected_sections)
          AND st1.day = st2.day
          AND ts1.start_time < ts2.end_time
          AND ts1.end_time > ts2.start_time
          AND sec1.term = sec2.term
          AND sec1.session = sec2.session
          AND sec1.year = sec2.year
    );
    IF conflict_count > 0 THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Time conflict detected with previously enrolled courses';
    END IF;
    

    CALL CheckPrereqsMet(student_id, selected_sections);
    CALL CheckCoreqsMet(student_id, selected_sections);
    SET anti_req_violations = (
        SELECT COUNT(*)
        FROM course_req cr
        WHERE cr.course_id IN (SELECT course_id FROM section WHERE FIND_IN_SET(id, selected_sections))
          AND cr.type = 'antireq'
          AND cr.req_id IN (
              SELECT DISTINCT s.course_id
              FROM section s
              JOIN enrollment e ON e.section_id = s.id
              WHERE e.student_id = student_id
              UNION
              SELECT DISTINCT s.course_id
              FROM section s
              WHERE FIND_IN_SET(s.id, selected_sections)
          )
    );
    IF anti_req_violations > 0 THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Anti-requisite violated for this course';
    END IF;
    

   
    -- check the total credit limit
    WITH selected_credits AS (
        SELECT
            sec.year,
            sec.term,
            sec.session,
            SUM(c.credits) AS total_credits
        FROM section sec
        JOIN course c ON sec.course_id = c.id
        WHERE FIND_IN_SET(sec.id, selected_sections)
        GROUP BY sec.year, sec.term, sec.session
    ),
    enrolled_credits AS (
        SELECT
            sec.year,
            sec.term,
            sec.session,
            SUM(c.credits) AS total_credits
        FROM enrollment e
        JOIN section sec ON e.section_id = sec.id
        JOIN course c ON sec.course_id = c.id
        WHERE e.student_id = student_id
        GROUP BY sec.year, sec.term, sec.session
    ),
    combined_credits AS (
        SELECT
            sc.year,
            sc.term,
            sc.session,
            COALESCE(sc.total_credits, 0) + COALESCE(ec.total_credits, 0) AS total_credits
        FROM selected_credits sc
        LEFT JOIN enrolled_credits ec
          ON sc.year = ec.year AND sc.term = ec.term AND sc.session = ec.session
    )
    SELECT COUNT(*)
    INTO credit_exceeded_count
    FROM combined_credits cc
    JOIN credit_limit cl
      ON cc.year = cl.year AND cc.term = cl.term AND cc.session = cl.session AND cl.student_id = student_id
    WHERE cc.total_credits > cl.credit_limit;
    IF credit_exceeded_count > 0 THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Credit limit exceeded for one or more terms';
    END IF;

    -- check the section capacity
     SET over_capacity_count = (
        SELECT COUNT(*)
        FROM section s
        LEFT JOIN enrollment e ON s.id = e.section_id
        WHERE FIND_IN_SET(s.id, selected_sections)
        GROUP BY s.id, s.capacity
        HAVING COUNT(e.student_id) >= s.capacity
    );
    
    IF over_capacity_count > 0 THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'One or more selected sections are over capacity';
    END IF;
    

    -- insert valid courses into enrollment
    INSERT INTO enrollment (student_id, section_id, grade)
    SELECT student_id, id, NULL
    FROM section
    WHERE FIND_IN_SET(id, selected_sections);
    
    -- clear enrolled courses from shopping cart
    SET SQL_SAFE_UPDATES = 0; 
    DELETE FROM shopping
    WHERE student_id = student_id
      AND FIND_IN_SET(section_id, selected_sections);
    SET SQL_SAFE_UPDATES = 1; 
    COMMIT;

END$$
DELIMITER ;



-- CALL enroll_selected_courses('yg202', '55,56');




DROP TRIGGER IF EXISTS check_section_time_insert_validity;
DELIMITER $$

CREATE TRIGGER check_section_time_insert_validity
BEFORE INSERT ON section_time
FOR EACH ROW
BEGIN
    DECLARE room_conflict_count INT;
    DECLARE instructor_conflict_count INT;

    -- Check if the room is already occupied at the same time
    SELECT COUNT(*)
    INTO room_conflict_count
    FROM section s
    JOIN section_time st1 ON s.id = st1.section_id
    JOIN time_slot ts1 ON st1.time_slot_id = ts1.id
    JOIN time_slot ts2 ON NEW.time_slot_id = ts2.id
    WHERE s.building_name = (SELECT building_name FROM section WHERE id = NEW.section_id)
      AND s.room_name = (SELECT room_name FROM section WHERE id = NEW.section_id)
      AND s.id != NEW.section_id
      AND s.year = (SELECT year FROM section WHERE id = NEW.section_id)
      AND s.term = (SELECT term FROM section WHERE id = NEW.section_id)
      AND s.session = (SELECT session FROM section WHERE id = NEW.section_id)
      AND st1.day = NEW.day
      AND ts1.start_time < ts2.end_time
      AND ts1.end_time > ts2.start_time;

    IF room_conflict_count > 0 THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Room is already occupied at the same time by another section';
    END IF;
END$$



DELIMITER ;

DROP TRIGGER IF EXISTS check_section_time_update_validity;

DELIMITER $$

CREATE TRIGGER check_section_time_update_validity
BEFORE UPDATE ON section_time
FOR EACH ROW
BEGIN
    DECLARE room_conflict_count INT;
    DECLARE instructor_conflict_count INT;

    -- Check if the updated room is already occupied at the same time
    SELECT COUNT(*)
    INTO room_conflict_count
    FROM section s
    JOIN section_time st1 ON s.id = st1.section_id
    JOIN time_slot ts1 ON st1.time_slot_id = ts1.id
    JOIN time_slot ts2 ON NEW.time_slot_id = ts2.id
    WHERE s.building_name = (SELECT building_name FROM section WHERE id = NEW.section_id)
      AND s.room_name = (SELECT room_name FROM section WHERE id = NEW.section_id)
      AND s.id != NEW.section_id
      AND s.year = (SELECT year FROM section WHERE id = NEW.section_id)
      AND s.term = (SELECT term FROM section WHERE id = NEW.section_id)
      AND s.session = (SELECT session FROM section WHERE id = NEW.section_id)
      AND st1.day = NEW.day
      AND ts1.start_time < ts2.end_time
      AND ts1.end_time > ts2.start_time;

    IF room_conflict_count > 0 THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Room is already occupied at the same time by another section';
    END IF;

    -- Check if the updated instructor has a time conflict
    SELECT COUNT(*)
    INTO instructor_conflict_count
    FROM teaches t
    JOIN section_time st1 ON t.section_id = st1.section_id
    JOIN time_slot ts1 ON st1.time_slot_id = ts1.id
    JOIN time_slot ts2 ON NEW.time_slot_id = ts2.id
    JOIN section s ON t.section_id = s.id
    WHERE t.instructor_id = (
        SELECT instructor_id
        FROM teaches
        WHERE section_id = NEW.section_id
    )
      AND t.section_id != NEW.section_id
      AND st1.day = NEW.day
      AND ts1.start_time < ts2.end_time
      AND ts1.end_time > ts2.start_time
      AND s.year = (SELECT year FROM section WHERE id = NEW.section_id)
      AND s.term = (SELECT term FROM section WHERE id = NEW.section_id)
      AND s.session = (SELECT session FROM section WHERE id = NEW.section_id);

    IF instructor_conflict_count > 0 THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Instructor has a time conflict with another section';
    END IF;
END$$

DELIMITER ;

-- insert into section (course_id, type, term, session, year, capacity, building_name, room_name) values 
-- ('COMPSCI 101', 'SEM', 'Fall', 'first', 2024, 60, 'IB', '3106');

-- insert into section_time (section_id, time_slot_id, day) values 
-- (973, 4, 'Mon');

-- UPDATE section_time
-- SET time_slot_id = 7,
--     day = 'tue'
-- WHERE section_id = 2;


DROP TRIGGER IF EXISTS check_teaches_insert;

DELIMITER $$

CREATE TRIGGER check_teaches_insert
BEFORE INSERT ON teaches
FOR EACH ROW
BEGIN
    DECLARE time_conflict_count INT;

    -- Check for time conflicts
    SELECT COUNT(*)
    INTO time_conflict_count
    FROM teaches t
    JOIN section_time st1 ON t.section_id = st1.section_id
    JOIN time_slot ts1 ON st1.time_slot_id = ts1.id
    JOIN section_time st2 ON st2.section_id = NEW.section_id
    JOIN time_slot ts2 ON st2.time_slot_id = ts2.id
    JOIN section s1 ON t.section_id = s1.id
    JOIN section s2 ON NEW.section_id = s2.id
    WHERE t.instructor_id = NEW.instructor_id
      AND st1.day = st2.day
      AND ts1.start_time < ts2.end_time
      AND ts1.end_time > ts2.start_time
      AND s1.year = s2.year
      AND s1.term = s2.term
      AND s1.session = s2.session;
      
    IF time_conflict_count > 0 THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Instructor has a time conflict with another section';
    END IF;
END$$
DELIMITER ;


DROP TRIGGER IF EXISTS check_teaches_update;

DELIMITER $$

CREATE TRIGGER check_teaches_update
BEFORE UPDATE ON teaches
FOR EACH ROW
BEGIN
    DECLARE time_conflict_count INT;

    -- Check for time conflicts
    SELECT COUNT(*)
    INTO time_conflict_count
    FROM teaches t
    JOIN section_time st1 ON t.section_id = st1.section_id
    JOIN time_slot ts1 ON st1.time_slot_id = ts1.id
    JOIN section_time st2 ON st2.section_id = NEW.section_id
    JOIN time_slot ts2 ON st2.time_slot_id = ts2.id
    JOIN section s1 ON t.section_id = s1.id
    JOIN section s2 ON NEW.section_id = s2.id
    WHERE t.instructor_id = NEW.instructor_id
      AND t.section_id != OLD.section_id
      AND st1.day = st2.day
      AND ts1.start_time < ts2.end_time
      AND ts1.end_time > ts2.start_time
      AND s1.year = s2.year
      AND s1.term = s2.term
      AND s1.session = s2.session;

    IF time_conflict_count > 0 THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Instructor has a time conflict with another section';
    END IF;
END$$

DELIMITER ;


INSERT INTO teaches (instructor_id, section_id)
VALUES ('bl291', 650);

UPDATE teaches
SET section_id = 22
WHERE instructor_id = 'bl291' and section_id=650; 

DROP PROCEDURE IF EXISTS make_payment;
DELIMITER $$

CREATE PROCEDURE make_payment(
    IN student_id VARCHAR(50),
    IN payment_amount NUMERIC(10, 2)
)
BEGIN
    DECLARE current_outstanding_due NUMERIC(10, 2);
    
    SELECT due - paid INTO current_outstanding_due
    FROM balance
    WHERE student_id = student_id;

    -- Validate the payment amount
    IF current_outstanding_due IS NULL THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Student ID not found in balance table';
    ELSEIF payment_amount <= 0 THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Payment amount must be greater than 0';
    ELSEIF payment_amount > current_outstanding_due THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Payment amount exceeds outstanding due';
    END IF;

    UPDATE balance
    SET 
        outstanding_due = outstanding_due - payment_amount,
        paid = paid + payment_amount
    WHERE student_id = student_id;
    -- Log success message
    SELECT CONCAT('Payment of ', payment_amount, ' applied for student ID ', student_id) AS payment_status;
END$$

DELIMITER ;


DELIMITER $$

DROP PROCEDURE IF EXISTS swap_course;
CREATE PROCEDURE swap_course(
    IN student_id VARCHAR(50),
    IN drop_section_id INT, -- The section ID to drop
    IN enroll_section_ids TEXT -- Comma-separated list of section IDs to enroll
)
BEGIN
    DECLARE drop_count INT;

    -- Step 1: Check if the student is actually enrolled in the course to be dropped
    SELECT COUNT(*) INTO drop_count
    FROM enrollment
    WHERE student_id = student_id
      AND section_id = drop_section_id;

    IF drop_count = 0 THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Student is not enrolled in the section to be dropped';
    END IF;

    -- Step 2: Drop the specified course
    DELETE FROM enrollment
    WHERE student_id = student_id
      AND section_id = drop_section_id;

    -- Step 3: Enroll in the new sections
    CALL enroll_selected_courses(student_id, enroll_section_ids);

    -- Step 4: Log the successful swap
    SELECT CONCAT(
        'Successfully swapped section ', drop_section_id, 
        ' with new sections: ', enroll_section_ids
    ) AS swap_status;
END$$

DELIMITER ;

-- example usage
-- CALL swap_course('yg202', 55, '56');
