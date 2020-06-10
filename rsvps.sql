USE sjin$sjin;
drop table if exists rsvps;
create table rsvps(
    rsvpid int NOT NULL AUTO_INCREMENT,

    eid int,
    eName varchar(50),
    orgName varchar(50),
    rsvp int default 0,
    postedat DATETIME DEFAULT CURRENT_TIMESTAMP,
    orgid int,
    primary key (rsvpid)
    )

