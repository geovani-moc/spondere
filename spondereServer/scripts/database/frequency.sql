create table frequency(
    studentUsername varchar(20),
    academicClassID integer,
    attendanceMethod integer not null,
    createDate timestamp not null,
    geolocalization point,
    validationType integer,
    photo bytea,
    constraint frequency_pk primary key (academicClassID, studentUsername),
    constraint academicClassID_fk foreign key (academicClassID) references academicClass(id)
);