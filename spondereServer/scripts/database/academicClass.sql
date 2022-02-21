create table academicClass(
    id serial,
    groupID integer not null,
    titleClass varchar(50) not null,
    descriptionClass varchar(300) not null,
    beginDate timestamp with time zone,
    endDate timestamp with time zone,
    longitude decimal,
    latitude decimal,
    activeValidation boolean default false not null,
    validationByQrCode boolean default false not null,
    validationByBLE boolean default false not null,
    blockedAttendance boolean default false not null,
    validationCode varchar(10),
    constraint academicClass_pk primary key (id),
    constraint group_fk foreign key (groupID) references groups(id)
);