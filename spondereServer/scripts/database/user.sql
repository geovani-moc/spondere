create table users(
    code varchar(10),
    password varchar(60) not null,
    username varchar(20) not null,
    status integer not null,
    email varchar(40),
    fullName varchar(40) not null,
    disabled boolean not null,
    constraint user_pk primary key(code)
);