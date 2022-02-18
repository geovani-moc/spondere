create table frequency(
    id serial,
    studentID integer,
    academicClassID integer,
    manualAttendance boolean default false not null,
    BLEAttendance boolean default false not null,
    QrCodeAttendance boolean default false not null,
    createDate timestamp not null,
    validationCode varchar(10),
    latitude varchar(20),
    longitude varchar(20),
    failure varchar(50),
    photo bytea,
    constraint frequency_pk primary key (id),
    constraint academicClassID_fk foreign key (academicClassID) references academicClass(id),
    constraint studentID_fk foreign key (studentID) references users(id)
);