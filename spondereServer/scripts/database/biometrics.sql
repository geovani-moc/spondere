create table biometrics(
    id serial,
    studentID integer,
    createDate timestamp,
    deactivate boolean default false not null,
    invalid boolean default false not null,
    constraint biometrics_fk primary key(id),
    constraint student_fk foreign key(studentID) references users(id)
);