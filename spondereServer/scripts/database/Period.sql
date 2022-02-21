create table period(
    id serial,
    code varchar(10) not null,
    active boolean default true not null,
    beginDate timestamp with time zone not null,
    endDate timestamp with time zone not null,
    constraint period_pk primary key(id),
    unique(code)
);