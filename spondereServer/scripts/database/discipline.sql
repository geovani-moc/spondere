create table discipline(
    code varchar(10),
    semesterCode varchar(10),
    name varchar(30),
    description varchar(50),
    constraint discipline_pk primary key(code),
    constraint period_pk foreign key(semesterCode) references period(code)
);