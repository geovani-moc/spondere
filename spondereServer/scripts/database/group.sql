create table groups(
    id serial,
    code varchar(20) not null,
    active boolean default true not null,
    semesterID integer not null,
    disciplineID integer not null,
    constraint group_pk primary key (id),
    constraint discipline_fk foreign key(disciplineID) references discipline(id),
    constraint period_fk foreign key(semesterID) references period(id),
    unique(code)
);