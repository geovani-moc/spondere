create table group_professors(
    professorCode varchar(10),
    groupCode varchar(10),
    constraint group_professors_pk primary key(professorCode, groupCode),
    constraint professor_fk foreign key(professorCode) references users(code),
    constraint group_fk foreign key(groupCode) references groups(code)
);