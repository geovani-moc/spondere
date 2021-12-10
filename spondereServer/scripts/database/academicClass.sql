create table academicClass(
    code varchar(10),
    groupCode varchar(10),
    classNumber integer not null,
    titleClass varchar(20),
    description varchar(100),
    beginDate timestamp,
    endDate timestamp,
    validationStatus integer,
    validationType integer,
    validationCode varchar(10),
    constraint academicClass_pk primary key (code),
    constraint group_fk foreign key (groupCode) references groups(code)
);