create table discipline(
    id serial,
    code varchar(20) not null,
    name varchar(50) not null,
    description varchar(300),
    constraint discipline_pk primary key(id),
    unique(code)
);