create table group_students(
    studentCode varchar(10),
    groupCode varchar(10),
    constraint group_students_pk primary key(studentCode, groupCode),
    constraint student_fk foreign key(studentCode) references users(code),
    constraint group_fk foreign key(groupCode) references groups(code)
);