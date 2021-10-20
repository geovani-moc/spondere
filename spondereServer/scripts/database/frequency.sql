create table frequency(
    studentCode varchar(10),
    academicClassCode varchar(10),
    attendaceMethod integer not null,
    createDate timestamp not null,
    geolocalization varchar(21),
    validationType integer,
    photo bytea,
    constraint frequency_pk primary key (studentCode, academicClassCode),
    constraint studentCode_fk foreign key (studentCode) references users(code),
    constraint academicClassCode_fk foreign key (academicClassCode) references academicClass(code)
);