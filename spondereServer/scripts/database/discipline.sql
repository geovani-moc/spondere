create table discipline(
    id serial,
    semesterID integer,
    name varchar(30),
    description varchar(200),
    constraint discipline_pk primary key(id),
    constraint period_fk foreign key(semesterID) references period(id)
);