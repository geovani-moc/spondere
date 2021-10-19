create table frequency(
    studentCode varchar(10),
    academicClassCode integer,
    method integer,
    createDate timestamp not null,
    geolocalization varchar(21),
    validationType integer not null,
    photo bytea,
    constraint frequency_pk primary key (studentCode, academicClassCode),
    constraint studentCode_fk foreign key (studentCode) references users(code),
    constraint academicClassCode_fk foreign key (academicClassCode) references academicClass(code)
);