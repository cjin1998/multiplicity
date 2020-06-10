USE sjin$sjin;
drop table if exists events;
create table events(
    eid int NOT NULL AUTO_INCREMENT,
    postedat DATETIME DEFAULT CURRENT_TIMESTAMP,
    eName varchar(50),
    orgid int,
    orgName varchar(50),
    eDate date,
    eTime time,
    location varchar(50),
    address1 varchar(50),
    address2 varchar(50),
    eState varchar(50),
    eZip varchar(50),
    eBio varchar(500),
    rsvp int default 0,
    primary key (eid)
    )
