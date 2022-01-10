create table users(
    id serial,
    username varchar(20) not null,
    password varchar(60) not null,
    email varchar(40),
    fullName varchar(40) default false not null,
    disabled boolean default false not null,
    professor boolean default false not null,
    student boolean default false not null,
    administrator boolean default false not null,
    constraint user_pk primary key(id),
    unique (username)
);