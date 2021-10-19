create table groups(
    classCode varchar(10),
    ProfessorCode varchar(10),
    studentCode varchar(10),
    constraint group_pk primary key (classCode),
    constraint professor_fk foreign key(ProfessorCode) references users(code),
    constraint student_fk foreign key(studentCode) references users(code)
);