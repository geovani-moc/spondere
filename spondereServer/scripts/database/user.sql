create table user(
    username varchar(20) not null,
    code varchar(10),
    -- faceFeatures integer [],
    password varchar(40) not null,
    status integer not null,
    email varchar(40),
    fullName varchar(40) not null,
    disabled boolean not null,

    constraint user_pk primary key(code)

);