create table group_students(
    studentUsername varchar(20),
    groupID integer,
    constraint group_students_pk primary key(groupID, studentUsername),
    constraint student_fk foreign key(studentUsername) references users(username),
    constraint group_fk foreign key(groupID) references groups(id)
);