create table groups(
    code varchar(10),
    beginDate timestamp,
    endDate timestamp,
    groupStatus integer,
    disciplineCode varchar(10),
    constraint group_pk primary key (code),
    constraint discipline_fk foreign key(disciplineCode) references discipline(code)
);