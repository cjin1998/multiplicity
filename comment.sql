USE sjin$sjin;
drop table if exists comment;

 create table comment(
    commentid int NOT NULL AUTO_INCREMENT,
    postedat DATETIME DEFAULT CURRENT_TIMESTAMP,
    postid int,
    content varchar(140),
    primary key(commentid)
)
