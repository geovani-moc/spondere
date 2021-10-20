create table users(
    username varchar(20) not null,
    code varchar(10),
    password varchar(40) not null,
    status integer not null,
    email varchar(40),
    fullName varchar(40) not null,
    disabled boolean not null,
    constraint user_pk primary key(code),
    constraint username_unq unique(username)
);