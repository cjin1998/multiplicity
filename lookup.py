import dbi

DSN = None
#contains most of our SQL statements so that our app.py is not too clunky
def getConn(db):
    '''returns a database connection to the given database'''
    global DSN
    if DSN is None:
        DSN = dbi.read_cnf()
    conn = dbi.connect(DSN)
    conn.select_db(db)
    return conn


def getAllPosts(conn):
    curs = dbi.dictCursor(conn)
    curs.execute("select * from post order by pid DESC")
    return curs.fetchall()

def insertPost(conn, postedat, poster, theme, thing):
    curs = dbi.dictCursor(conn)
    curs.execute('insert into post (postedat, poster, theme, thing) values (%s, %s, %s, %s)', [postedat, poster, theme, thing]) 
    return True

def getEvents(conn,eName):
    curs = dbi.dictCursor(conn)
    curs.execute("select * from events where eDate>= CURDATE() AND (eName like %s OR location like %s OR eDate like %s) order by eDate ASC", ['%'+eName+'%', '%'+eName+'%', '%'+eName+'%' ])
    return curs.fetchall()

def getAllEvents(conn):
    curs = dbi.dictCursor(conn)
    curs.execute("select * from events where eDate>= CURDATE() order by eDate ASC")
    return curs.fetchall()

def insertEvents(conn, eName, orgid, orgName, eDate, eTime, location, eBio):
    curs = dbi.dictCursor(conn)
    curs.execute('insert into events (eName, orgid, orgName, eDate, eTime, location, eBio) values (%s, %s, %s, %s, %s, %s, %s)', [eName, orgid, orgName, eDate, eTime, location, eBio]) 
    return True
                               
def getMembers(conn,name):
    curs = dbi.dictCursor(conn)
    curs.execute("select * from member where name like %s", ['%'+name+'%'])
    return curs.fetchall()

def getAllMembers(conn):
    curs = dbi.dictCursor(conn)
    curs.execute("select * from member")
    return curs.fetchall()

def insertMember(conn, name, orgMail, password, bio, link, cell, filename):
    curs = dbi.dictCursor(conn)
    curs.execute('insert into member (name, orgMail, password, bio, link, cell, pic) values (%s, %s, %s, %s, %s, %s, %s)', [name, orgMail, password, bio, link, cell, filename]) 
    return True

def addStaff(conn, orgid, sName, sEmail, sTitle, filename):
    curs = dbi.dictCursor(conn)
    curs.execute('insert into staff (orgid, sName, sEmail, sTitle,pic) values (%s, %s, %s, %s, %s)', [orgid, sName, sEmail, sTitle, filename]) 
    return True

def collab(conn, orgid, sName, vorgid, rName, msg):
    curs = dbi.dictCursor(conn)
    curs.execute('insert into collab (orgid, sName, vorgid, rName, msg) values (%s, %s, %s, %s, %s)', [orgid, sName, vorgid, rName, msg]) 
    return True

def updateMemberPic(conn, id, name, orgMail, password, bio, link, cell, filename): 
    curs = dbi.dictCursor(conn)
    curs.execute('insert into member values (%s, %s, %s, %s, %s, %s, %s, %s) ON DUPLICATE KEY UPDATE name=%s, orgMail=%s, password=%s, bio=%s,link=%s, cell=%s, pic=%s' , [id, name, orgMail, password, bio, link, cell, filename, name, orgMail, password, bio, link, cell, filename]) 
    return True

def updateMember(conn, id, name, orgMail, password, bio, link, cell): 
    curs = dbi.dictCursor(conn)
    curs.execute('insert into member (orgid, name, orgMail, password, bio, link, cell) values (%s, %s, %s, %s, %s, %s, %s) ON DUPLICATE KEY UPDATE name=%s, orgMail=%s, password=%s, bio=%s,link=%s, cell=%s' , [id, name, orgMail, password, bio, link, cell, name, orgMail, password, bio, link, cell]) 
    return True
