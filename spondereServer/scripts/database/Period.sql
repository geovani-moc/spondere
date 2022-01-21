create table period(
    id serial,
    code varchar(10),
    active boolean default true not null,
    beginDate timestamp,
    endDate timestamp,
    constraint period_pk primary key(id),
    unique(code)
);