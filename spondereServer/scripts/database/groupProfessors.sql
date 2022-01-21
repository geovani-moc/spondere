create table group_professors(
    professorUsername varchar(20),
    groupID integer,
    constraint group_professors_pk primary key(groupID, professorUsername),
    constraint professor_fk foreign key(professorUsername) references users(username),
    constraint group_fk foreign key(groupID) references groups(id)
);