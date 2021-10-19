create table academicClass(
    code integer,
    disciplineCode varchar(10) not null,
    professorCode varchar(10) not null,
    beginDate timestamp,
    endDate timestamp,
    constraint academicClass_pk primary key (code),
    constraint discipline_fk foreign key (disciplineCode) references discipline(code),
    constraint professor_fk foreign key (professorCode) references users(code)
);