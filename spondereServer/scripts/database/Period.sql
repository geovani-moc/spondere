create table period(
    id serial,
    code varchar(10),
    beginDate timestamp,
    endDate timestamp,
    constraint period_pk primary key(id),
    unique(code)
)