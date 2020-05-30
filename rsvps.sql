USE sjin$sjin;
drop table if exists rsvps;
create table rsvps(
    rsvpid int NOT NULL AUTO_INCREMENT,
    eid int,
    orgName varchar(50),
    rsvp int default 0,
    primary key (rsvpid)
    )

