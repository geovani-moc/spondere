create table biometrics(
    studentCode varchar(10),
    createDate timestamp,
    status integer,
    constraint biometrics_fk primary key(studentCode),
    constraint student_fk foreign key(studentCode) references users(code)
);