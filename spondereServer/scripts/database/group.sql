create table groups(
    code varchar(10),
    beginDate timestamp,
    endDate timestamp,
    groupStatus integer,
    constraint group_pk primary key (code)
);