create table frequency(
    id serial,
    studentID integer not null,
    academicClassID integer not null,
    manualAttendance boolean default false not null,
    BLEAttendance boolean default false not null,
    QrCodeAttendance boolean default false not null,
    createDate timestamp with time zone not null,
    validationCode varchar(10),
    latitude decimal,
    longitude decimal,
    failure varchar(50),
    photo bytea,
    constraint frequency_pk primary key (id),
    constraint academicClassID_fk foreign key (academicClassID) references academicClass(id),
    constraint studentID_fk foreign key (studentID) references users(id)
);