create table groups(
    id serial,
    beginDate timestamp,
    endDate timestamp,
    deactivate boolean default false not null,
    disciplineID integer,
    constraint group_pk primary key (id),
    constraint discipline_fk foreign key(disciplineID) references discipline(id)
);