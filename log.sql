use sjin;
drop table if exists log;
create table log(
    orgid int,
    postedat DATETIME DEFAULT CURRENT_TIMESTAMP,
    primary key(orgid)
) 
