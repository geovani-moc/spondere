create table academicClass(
    id serial,
    groupID integer,
    titleClass varchar(20),
    descriptionClass varchar(100),
    beginDate timestamp,
    endDate timestamp,
    validationStatus integer,
    validationType integer,
    validationCode varchar(10),
    constraint academicClass_pk primary key (id),
    constraint group_fk foreign key (groupID) references groups(id)
);