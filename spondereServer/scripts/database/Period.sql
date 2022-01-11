create table period(
    id serial,
    code varchar(10),
    beginDate timestamp,
    endDate timestamp,
    deactivate boolean default false not null,
    constraint period_pk primary key(id),
    unique(code)
)