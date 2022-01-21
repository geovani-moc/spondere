create table discipline(
    id serial,
    code varchar(20),
    name varchar(50),
    description varchar(300),
    constraint discipline_pk primary key(id),
    unique(code)
);