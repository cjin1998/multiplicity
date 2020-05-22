use sjin;
drop table if exists staff;
create table staff(
    sid int NOT NULL AUTO_INCREMENT,
    orgid int,
    sName varchar(50),
    sEmail varchar(50),
    sTitle varchar(50),
    pic varchar(50) DEFAULT NULL,
    primary key (sid)
)
