create table group_professors(
    groupID integer,
    professorUsername varchar(20),
    constraint group_professors_pk primary key(groupID, professorUsername),
    constraint professor_fk foreign key(professorUsername) references users(username),
    constraint group_fk foreign key(groupID) references groups(id)
);