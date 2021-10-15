create table group(
    classCode varchar(10),
    ProfessorCode varchar(10),
    studentCode varchar(10),
    
    constraint group_pk primary key (classCode)
    constraint professor_fk foreign key(ProfessorCode) references user(code)_
    constraint student_fk foreign key(studentCode) references user(code)_
);