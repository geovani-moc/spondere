create table frequency(
    studentCode varchar(10),
    academicClassCode varchar(10),
    method integer,
    createDate timestamp not null,
    geolocalization varchar(21),
    validationType integer not null,
    photo integer[],

    constraint frequency_pk primary key (studentCode, academicClassCode),
    constraint studentCode_fk foreign key (studentCode) references user(code),
    constraint academicClassCode_fk foreign key (academicClassCode) references academicClass(academicClass_pk)
);