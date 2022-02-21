create table biometrics(
    id serial,
    studentID integer not null,
    createDate timestamp with time zone not null,
    active boolean default true not null,
    invalid boolean default false not null,
    failure varchar(50),
    constraint biometrics_fk primary key(id),
    constraint student_fk foreign key(studentID) references users(id)
);