USE sjin$sjin;
drop table if exists post;

 create table post(
    pid int NOT NULL AUTO_INCREMENT,
    postedatt DATETIME DEFAULT CURRENT_TIMESTAMP,
    postedat varchar(50),
    poster varchar(50),
    theme varchar(50),
    thing varchar(200),
    primary key(pid)
)

