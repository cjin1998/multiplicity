USE sjin$sjin;
drop table if exists member;
create table member(
    orgid int NOT NULL AUTO_INCREMENT,
    name varchar(50),
    orgMail varchar(50),
    password varchar(50),
    bio varchar(500),
    link varchar(50),
    cell varchar(50),
    pic varchar(50) DEFAULT NULL,
    primary key (orgid)
)

