from flask import (Flask, render_template, make_response, url_for, request,
                   redirect, flash, session, send_from_directory, jsonify
                   )

import os


from werkzeug.datastructures import FileStorage

from datetime import datetime

from flask_mail import Mail, Message

app = Flask(__name__)

app.config.update(
	DEBUG=True,
	#EMAIL SETTINGS
	MAIL_SERVER='smtp.gmail.com',
	MAIL_PORT=465,
	MAIL_USE_SSL=True,
	MAIL_USERNAME = 'outreach@multiplicity.io',
	MAIL_PASSWORD = 'ZSy%TrhTUY#E7a'
	)
mail = Mail(app)

 
import sys,os,random,lookup, dbi
import cryptography
import sys, os, random
import imghdr
import dbi
import bcrypt

 
app.secret_key = 'your secret here'
# replace that with a random key
app.secret_key = ''.join([ random.choice(('ABCDEFGHIJKLMNOPQRSTUVXYZ' +
                                          'abcdefghijklmnopqrstuvxyz' +
                                          '0123456789'))
                           for i in range(20) ])
 
# This gets us better error messages for certain common request errors

app.config['TRAP_BAD_REQUEST_ERRORS'] = True
app.config['UPLOADS'] = 'uploads'

app.config['MAX_CONTENT_LENGTH'] = 1*1024*1024 # 1 MB
def getConn(db):
    '''Returns a database connection for that db'''
    dsn = dbi.read_cnf()
    conn = dbi.connect(dsn)
    conn.select_db(db)
    return conn
 
#public homepage director 
@app.route('/')
def main():
    return render_template('main.html')

def sendmail(email, message, title):
    msg = Message(title, sender="outreach@multiplicity.io", recipients=[email])
    msg.body = message     
    mail.send(msg)
    return True


@app.route('/send_mail/', methods=["GET","POST"])
def send_mail():
    email=request.form['email']
    conn = lookup.getConn('sjin') 
    curs = dbi.dictCursor(conn)
    curs.execute('insert into member(orgMail) values (%s)', [email])
    curs.execute('select orgid from member where orgMail=%s', [email])
    row = curs.fetchone()
    orgid = str(row['orgid'])
    title= "Welcome to Multiplicity"
    link="\nhttp://149.130.210.46:1234/register/"+orgid
    message="here's the link to join multiplicity!" + link 
    sendmail(email, message, title)
    flash("An email has been sent to your account.")
    return redirect(request.referrer)

@app.route('/forgot/', methods=["GET","POST"])
def forgot():
    if request.method == 'GET':  
        return render_template('forgot.html')
    else: 
        email=request.form['email']
        conn = lookup.getConn('sjin') 
        curs = dbi.dictCursor(conn)
        curs.execute('select orgid, password from member where orgMail=%s', [email])
        row = curs.fetchone()
        password=row['password']
        title= "Retrieve your password"
        message="Here's your password :" + password
        sendmail(email, message, title)
        flash("An email containing your password has been sent to your account.")
        return redirect(url_for("main")) 
 
    
@app.route('/register/<id>', methods=['GET','POST'])
def register(id):
    if request.method == 'GET':  
        return render_template('register.html', id=id)
    elif request.method == 'POST':
        name=request.form['name']
        orgMail=request.form['orgMail']
        password=request.form['password']
        bio=request.form['bio']
        link=request.form['link']
        cell=request.form['cell']
        pcheck=request.form['pcheck']
        if (password == pcheck):
            pic = request.files['pic']
            #print(pic)
            user_filename = pic.filename
            #print(user_filename)
            ext = user_filename.split('.')[-1]
            if (ext == "jpeg" or ext =="png" or ext =="jpg"):
                aname = user_filename.split('.')[0]
                filename = '{}.{}'.format(aname,ext)
                pathname = os.path.join(app.config['UPLOADS'],filename)
                pic.save(pathname)
                #print(pic)
                conn = lookup.getConn('sjin')
                insertSuccessful = lookup.updateMemberPic(conn, id, name, orgMail, password, bio, link, cell, filename)
                if (insertSuccessful):
                    flash("Successfully registered new org " + name)
                else:
                    flash("Error registering")
                return redirect(url_for("main")) 
            else:
                flash('Incorrect format for picture')
                return redirect(request.referrer)
                  
        else:
            flash('password does not match')
            return redirect(request.referrer)

            


#login route
@app.route('/login/', methods=["GET", "POST"])
def login():
    if request.method == 'GET':  
        return render_template('login.html')
    elif request.method == 'POST':
        username = request.form['username']
        passwd = request.form['password']
        conn = lookup.getConn('sjin') 
        curs = dbi.dictCursor(conn)
        curs.execute("SELECT orgMail,password FROM member WHERE orgMail = %s",[username])
        row = curs.fetchone()
        if row is None:
            # Same response as wrong password,
            # so no information about what went wrong
            flash('The email address is not registered.')
            return redirect( url_for('main'))
        password = row['password']
        hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        hashed_str = hashed.decode('utf-8')
        password2 = bcrypt.hashpw(passwd.encode('utf-8'),hashed_str.encode('utf-8'))
        password2_str = password2.decode('utf-8')
        if password2_str ==  hashed_str:
            session['username'] = username
            session['logged_in'] = True
            conn = lookup.getConn('sjin') 
            curs = dbi.dictCursor(conn)
            curs.execute("SELECT * FROM member WHERE orgMail = %s",[username])
            row = curs.fetchone()
            orgid = row['orgid']
            name = row['name']
            session['name'] = name
            session['orgid'] = orgid
            print(session)
            return redirect(url_for('home', id = orgid))
        else:
            flash('Password incorrect. Please try again')
            return redirect( url_for('main'))

           
@app.route('/logout/<id>/')
def logout(id):
    conn = lookup.getConn('sjin') 
    curs = dbi.dictCursor(conn)
    curs.execute('delete from log where orgid=%s', [id])
    curs.execute('insert into log (orgid) values (%s)', [id])
    flash('You are now logged out.')
    return redirect( url_for('main') )
    

@app.route('/home/<id>/')
def home(id):
    conn = lookup.getConn('sjin') 
    curs = dbi.dictCursor(conn)
    curs.execute('select * from member where orgid=%s', [id])
    orgInfo = curs.fetchone()
   
    orgname=orgInfo['name']
    
    curs.execute('select * from staff where orgid=%s', [id])
    sInfo = curs.fetchall()
    curs.execute('select postedat from log where orgid=%s', [id])
    a = curs.fetchone()
    if (a):
        time=a['postedat']
        print(time)
        curs.execute('select * from collab where vorgid=%s AND postedat>= %s order by collabid DESC', [id, time])
        newcollab = curs.fetchall()
        cnum=len(newcollab)
        curs.execute('select * from events where orgid!=%s AND postedat>= %s AND eDate>= CURDATE() order by eid DESC', [id, time])
        newevents = curs.fetchall()
        enum=len(newevents)
        curs.execute('select * from post where poster!=%s AND postedatt>= %s order by pid DESC', [orgname, time])
        newposts = curs.fetchall()
        pnum=len(newposts)
    else:
        curs.execute('select * from collab where vorgid=%s', [id])
        newcollab = curs.fetchall()
        newevents=[]
        newposts=[]
        cnum=0
        pnum=0
        enum=0
    return render_template('myhome.html', data = orgInfo, staff_data = sInfo, new=newcollab, events=newevents, posts=newposts, cnum=cnum, enum=enum, pnum=pnum ) 

@app.route('/myProfile/<id>')
def myProfile(id):
    conn = lookup.getConn('sjin') 
    curs = dbi.dictCursor(conn)
    curs.execute('select * from member where orgid=%s', [id])
    orgInfo = curs.fetchone()
    curs.execute('select * from staff where orgid=%s', [id])
    sInfo = curs.fetchall()
    return render_template('myProfile.html', data = orgInfo, staff_data = sInfo) 

@app.route('/myEvents/<id>')
def myEvents(id):
    conn = lookup.getConn('sjin') 
    curs = dbi.dictCursor(conn)
    curs.execute('select * from member where orgid=%s', [id])
    orgInfo = curs.fetchone()
    curs.execute('select * from events where orgid=%s', [id])
    events = curs.fetchall()
    return render_template('myEvents.html', data = orgInfo,  events = events) 


@app.route('/pic/<id>')
def pic(id):
    conn = lookup.getConn('sjin') 
    curs = dbi.dictCursor(conn)
    curs.execute('select pic from member where orgid = %s', [id])
    row = curs.fetchone()
    return send_from_directory(app.config['UPLOADS'],row['pic'])

@app.route('/spic/<sid>')
def spic(sid):
    conn = lookup.getConn('sjin') 
    curs = dbi.dictCursor(conn)
    curs.execute('select pic from staff where sid = %s', [sid])
    row = curs.fetchone()
    return send_from_directory(app.config['UPLOADS'],row['pic'])

@app.route('/crequest/<id>')
def crequest(id):
    conn = lookup.getConn('sjin') 
    curs = dbi.dictCursor(conn)
    curs.execute('select * from member where orgid=%s', [id])
    orgInfo = curs.fetchone()
    curs.execute('select * from collab where orgid=%s', [id])
    sends = curs.fetchall()
    snum=len(sends)
    curs.execute('select * from collab where vorgid=%s', [id])
    receives = curs.fetchall()
    rnum=len(receives)
    return render_template('crequest.html', data = orgInfo,  sends = sends, receives = receives, snum=snum, rnum=rnum) 




@app.route('/update//<id>', methods=["GET", "POST"])
def update(id):
    conn = lookup.getConn('sjin')
    curs = dbi.dictCursor(conn)
    curs.execute('select * from member where orgid=%s', [id])
    orgInfo = curs.fetchone()
    if request.method=="GET": 
        return render_template('update.html', data=orgInfo)
    else:
        name=request.form['name']
        orgMail=request.form['orgMail']
        password=request.form['password']
        bio=request.form['bio']
        link=request.form['link']
        cell=request.form['cell']
        
        pic = request.files['pic']
        
        user_filename = pic.filename
        ext = user_filename.split('.')[-1]
        aname = user_filename.split('.')[0]
        filename = '{}.{}'.format(aname,ext)
        if (filename==""):
            insertSuccessful = lookup.updateMember(conn, id, name, orgMail, password, bio, link, cell)
            if (insertSuccessful):
                flash("Successfully updated org " + name)
            else:
                flash("Error updating")
            return redirect(url_for("myProfile", id = id))   
        else:
            pathname = os.path.join(app.config['UPLOADS'],filename)
            pic.save(pathname)
            insertSuccessful = lookup.updateMemberPic(conn, id, name, orgMail, password, bio, link, cell, filename)
            if (insertSuccessful):
                flash("Successfully updated org " + name)
            else:
                flash("Error updating")
            return redirect(url_for("myProfile", id = id))    


@app.route('/addStaff/<id>/', methods=['GET','POST'])
def addStaff(id):
    conn = lookup.getConn('sjin') 
    curs = dbi.dictCursor(conn)
    curs.execute('select * from member where orgid=%s', [id])
    orgInfo = curs.fetchone()
    if request.method == 'GET':  
        return render_template('addStaff.html', data=orgInfo)
    elif request.method == 'POST':
        orgid = id
        sName=request.form['sName']
        sTitle=request.form['sTitle']
        sEmail=request.form['sEmail']
        
        pic = request.files['pic']
        user_filename = pic.filename
        ext = user_filename.split('.')[-1]
        aname = user_filename.split('.')[0]
        filename = '{}.{}'.format(aname,ext)
        pathname = os.path.join(app.config['UPLOADS'],filename)
        pic.save(pathname)
        conn = lookup.getConn('sjin')
        insertSuccessful = lookup.addStaff(conn, orgid, sName, sEmail, sTitle, filename)
        if (insertSuccessful):
            flash("Successfully added a new staff " + sName)
        else:
            flash("Error adding staff")
        return redirect(url_for("myProfile", id = id))       

@app.route('/dstaff/<sid>/', methods=['GET','POST'])
def dstaff(sid):
    conn = lookup.getConn('sjin') 
    curs = dbi.dictCursor(conn)
    curs.execute('delete from staff where sid = %s', [sid])
    flash("staff was deleted successfully.")
    return redirect(request.referrer)  

@app.route('/devent/<eid>/', methods=['GET','POST'])
def devent(eid):
    conn = lookup.getConn('sjin') 
    curs = dbi.dictCursor(conn)
    curs.execute('delete from events where eid = %s', [eid])
    flash("event was deleted successfully.")
    return redirect(request.referrer) 

@app.route('/dcollab/<cid>/', methods=['GET','POST'])
def dcollab(cid):
    conn = lookup.getConn('sjin') 
    curs = dbi.dictCursor(conn)
    curs.execute('delete from collab where collabid = %s', [cid])
    flash("Collab Request was deleted successfully. The receiver will no longer see your collab request.")
    return redirect(request.referrer)  

@app.route('/dpost/<pid>/', methods=['GET','POST'])
def dpost(pid):
    conn = lookup.getConn('sjin') 
    curs = dbi.dictCursor(conn)
    curs.execute('delete from post where pid = %s', [pid])
    flash("post was deleted successfully.")
    return redirect(request.referrer) 


@app.route('/singleP/<id>/<vid>')
def singleP(id, vid):
    conn = lookup.getConn('sjin') 
    curs = dbi.dictCursor(conn)
    curs.execute('select * from member where orgid=%s', [id])
    orgInfo = curs.fetchone()
    curs.execute('select * from member where orgid=%s', [vid])
    vorgInfo = curs.fetchone()
    curs.execute('select * from staff where orgid=%s', [vid])
    sInfo = curs.fetchall()
    return render_template('singleP.html', data = orgInfo, vdata = vorgInfo, staff_data = sInfo) 

@app.route('/collab/<id>/<vid>', methods=['GET','POST'])
def collab(id, vid):
    conn = lookup.getConn('sjin') 
    curs = dbi.dictCursor(conn)
    curs.execute('select * from member where orgid=%s', [id])
    orgInfo = curs.fetchone()
    curs.execute('select * from member where orgid=%s', [vid])
    vorgInfo = curs.fetchone()
    if request.method == 'GET':  
        return render_template('collab.html', data = orgInfo, vdata = vorgInfo) 
    elif request.method == 'POST':
        orgid = id
        sName = orgInfo['name']
        vorgid = vid 
        rName = vorgInfo['name']
        rMail = vorgInfo['orgMail']
        title="Multiplicity Collab Request from " + sName
        msg=request.form['msg']
        message = msg
        sendmail(rMail, message, title)
        msg=request.form['msg']
        conn = lookup.getConn('sjin')
        insertSuccessful = lookup.collab(conn, orgid, sName, vorgid, rName, msg)
        if (insertSuccessful):
            flash("Successfully sent collab request to " + rName)
        else:
            flash("Error sending request")
        return redirect(url_for("members", id = id))   


@app.route('/rsvp/', methods=['GET','POST'])
def rsvp():
    eid = request.form['eid']
    conn = lookup.getConn('sjin') 
    curs = dbi.dictCursor(conn)
    curs.execute('select * from events where eid=%s', [eid])
    eInfo = curs.fetchone()
   
    postedat = eInfo['postedat']
    eName = eInfo['eName']
    orgid = eInfo['orgid']
    orgName = eInfo['orgName']
    eDate=eInfo['eDate']
    eTime=eInfo['eTime']
    location=eInfo['location']
    eBio=eInfo['eBio']
    rsvp=eInfo['rsvp']
    people = request.form['num']
    num = int(people)
    new = rsvp + num

    curs.execute('insert into events values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s) ON DUPLICATE KEY UPDATE rsvp=%s', [eid, postedat, eName, orgid, orgName, eDate, eTime, location, eBio, new, new]) 

    return jsonify({'error': False, 'eid': eid, 'num': new})


@app.route('/resources/<id>/')
def resources(id):
    conn = lookup.getConn('sjin') 
    curs = dbi.dictCursor(conn)
    curs.execute('select * from member where orgid=%s', [id])
    orgInfo = curs.fetchone()
    return render_template('resources.html', data = orgInfo) 


#member table and search bar            
@app.route('/member/<id>/',methods=["GET","POST"])
@app.route('/member/<id>/<ask>', methods=["GET","POST"])
def members(id, ask=None):
    conn = lookup.getConn('sjin') 
    curs = dbi.dictCursor(conn)
    curs.execute('select * from member where orgid=%s', [id])
    orgInfo = curs.fetchone()
    if request.method == 'POST':
        ask = request.form['search-name']
        return redirect(url_for('members', ask=ask, id=orgInfo['orgid']))
    else:
        if ask == None:
            member = lookup.getAllMembers(conn)
        else:
            member = lookup.getMembers(conn, ask)
        return render_template('member.html', 
                                member_data=member, orgInfo=orgInfo, data = orgInfo) 


@app.route('/events/<id>/',methods=["GET","POST"])
@app.route('/events/<id>/<ask>', methods=["GET","POST"])
def events(id, ask=None):
    conn = lookup.getConn('sjin') 
    curs = dbi.dictCursor(conn)
    curs.execute('select * from member where orgid=%s', [id])
    orgInfo = curs.fetchone()
    if request.method == 'POST':
        ask = request.form['search-event']
        if(ask):
            return redirect(url_for('events', ask=ask, id=orgInfo['orgid']))
        else: 
            ask = request.form['search-date']
            return redirect(url_for('events', ask=ask, id=orgInfo['orgid']))
    else:
        if ask == None:
            events = lookup.getAllEvents(conn)
        else:
            events = lookup.getEvents(conn, ask)
        return render_template('events.html', 
                                events_data=events, orgInfo=orgInfo, data = orgInfo)
                          

@app.route('/createEvents/<id>/', methods=['GET','POST'])
def createEvents(id):
    conn = lookup.getConn('sjin') 
    curs = dbi.dictCursor(conn)
    curs.execute('select * from member where orgid=%s', [id])
    orgInfo = curs.fetchone()
    if request.method == 'GET':  
        return render_template('createEvents.html', data=orgInfo)
    elif request.method == 'POST':
        eName=request.form['eName']
        orgid = id
        orgName = orgInfo['name']
        eDate=request.form['eDate']
        eTime=request.form['eTime']
        location=request.form['location']
        eBio=request.form['eBio']
        conn = lookup.getConn('sjin')
        insertSuccessful = lookup.insertEvents(conn, eName, orgid, orgName, eDate, eTime, location, eBio)
        if (insertSuccessful):
            flash("Successfully created a new events " + eName)
        else:
            flash("Error creating events")
        return redirect(url_for("events", id = id))         


#private forum page
@app.route('/pforum/<id>/')
def pforum(id):
    conn = lookup.getConn('sjin') 
    curs = dbi.dictCursor(conn)
    curs.execute('select * from member where orgid=%s', [id])
    orgInfo = curs.fetchone()
    username = orgInfo['name']
    posts = lookup.getAllPosts(conn)
    return render_template('privateForum.html', 
                            post_data=posts, data=orgInfo, username = username)


#insert a post on private page
@app.route('/ppost/<id>/', methods=['GET','POST'])
def ppost(id):
    conn = lookup.getConn('sjin') 
    curs = dbi.dictCursor(conn)
    curs.execute('select * from member where orgid=%s', [id])
    orgInfo = curs.fetchone()
    if request.method == 'GET':  
        return render_template('insertPPost.html', data = orgInfo)
    elif request.method == 'POST':
        now = datetime.now()
        postedat = now.strftime("%d/%m/%Y %H:%M:%S")
        poster=orgInfo['name']
        theme=request.form['theme']
        thing=request.form['thing']
        conn = lookup.getConn('sjin')
        insertSuccessful = lookup.insertPost(conn, postedat, poster, theme, thing)
        if (insertSuccessful):
            print("posted by " + poster)
            flash("Successfully posted "+ theme)
        else:
            flash("Error")
        return redirect(url_for("pforum", id=id))   

#ajax route for comments
@app.route('/commentAjax/', methods=['GET','POST'])
def commentAjax():
     if request.method == 'GET':  
        #getting the id of the post
        postid = request.args['postid']
        conn = getConn('sjin')
        curs = dbi.dictCursor(conn)
        #getting all the comments with the postid from the comment database
        curs.execute("SELECT commentid, content FROM comment WHERE postid = %s",[postid])
        matches = curs.fetchall()
        return jsonify({'error': False, 'postid': postid, 'matches': matches})
     else:
        #getting postid and comment from the request form
        postid = request.form['cu']
        comment = request.form['comment']
        conn = getConn('sjin')
        curs = dbi.dictCursor(conn)
        #store the comment in the comment table
        curs.execute('insert into comment (postid, content) values (%s, %s)', [postid, comment]) 
        return jsonify({'error': False, 'postid': postid, 'comment': comment})
 
if __name__ == '__main__':
    import os
    uid = "1234"
    app.debug = True
    app.run('0.0.0.0',uid)

