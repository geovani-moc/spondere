create table academicClass(
    id serial,
    groupID integer,
    titleClass varchar(50) not null,
    descriptionClass varchar(300),
    beginDate timestamp,
    endDate timestamp,
    activeValidation boolean default false not null,
    validationByQrCode boolean default false not null,
    validationByBLE boolean default false not null,
    validationCode varchar(10),
    constraint academicClass_pk primary key (id),
    constraint group_fk foreign key (groupID) references groups(id)
);