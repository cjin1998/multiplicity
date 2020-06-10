USE sjin$sjin;
drop table if exists noti;
create table noti(
    orgid int,
    postedat DATETIME DEFAULT CURRENT_TIMESTAMP,
    unchecked int,
    primary key(orgid)
)
