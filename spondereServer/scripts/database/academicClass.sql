create table academicClass(
    id serial,
    groupID integer,
    titleClass varchar(50),
    descriptionClass varchar(200),
    beginDate timestamp,
    endDate timestamp,
    validationStatus integer,
    validationType integer,
    validationCode varchar(10),
    constraint academicClass_pk primary key (id),
    constraint group_fk foreign key (groupID) references groups(id)
);