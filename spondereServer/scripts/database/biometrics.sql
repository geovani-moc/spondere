create table biometrics(
    code varchar(10),
    createDate timestamp,
    status integer,
    studentCode varchar(10),
    constraint biometrics_fk primary key(code),
    constraint student_fk foreign key(studentCode) references users(code)
);