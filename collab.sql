use sjin;
drop table if exists collab;
create table collab(
    collabid int NOT NULL AUTO_INCREMENT,
    postedat DATETIME DEFAULT CURRENT_TIMESTAMP,
    orgid int,
    sName varchar(50),
    vorgid int,
    rName varchar(50),
    msg varchar(500),
    primary key (collabid)
)