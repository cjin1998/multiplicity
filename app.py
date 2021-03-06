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
	MAIL_USERNAME = 'christinejin9@gmail.com',
	MAIL_PASSWORD = '8hZ47vU3',
    USE_HTTPS = False
	)
mail = Mail(app)



import sys,os,random,lookup, dbi
import cryptography
import sys, os, random
import imghdr

import dbo
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
    dsn = dbo.read_cnf()
    conn = dbo.connect(dsn)
    conn.select_db(db)
    return conn

#public homepage director
@app.route('/')
def main():
    return render_template('main.html')

def sendmail(email, message, title):
    msg = Message(title, sender="christinejin9@gmail.com", recipients=[email])
    msg.body = message
    mail.send(msg)
    return True


@app.route('/send_mail/', methods=["GET","POST"])
def send_mail():
    email=request.form['email']
    emailList = ["shuyijin@mit.edu", "8@gmail.com"]
    conn = lookup.getConn('sjin$sjin')
    curs = dbo.dictCursor(conn)
    if email in emailList:
        curs.execute('insert into member(orgMail) values (%s)', [email])
        curs.execute('select orgid from member where orgMail=%s', [email])
        row = curs.fetchone()
        orgid = str(row['orgid'])
        title= "Register link"
        link="\nhttp://sjin.pythonanywhere.com/register/"+orgid
        message="Here's the link to join multiplicity!" + link
        sendmail(email, message, title)
    else:
        title= "Instruction on How to Join Multiplicity"
        link="message provided by Kaila"
        message="Here's the instruction to join multiplicity!" + link
        sendmail(email, message, title)
    flash("An email has been sent to your account.")
    conn.close()
    return redirect(request.referrer)

@app.route('/forgot/', methods=["GET","POST"])
def forgot():
    if request.method == 'GET':
        return render_template('forgot.html')
    else:
        email=request.form['email']
        conn = lookup.getConn('sjin$sjin')
        curs = dbo.dictCursor(conn)
        curs.execute('select orgid, password from member where orgMail=%s', [email])
        row = curs.fetchone()
        password=row['password']
        title= "Retrieve your password"
        message="Here's your password :" + password
        sendmail(email, message, title)
        flash("An email containing your password has been sent to your account.")
        conn.close()
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

            user_filename = pic.filename

            ext = user_filename.split('.')[-1]
            if (ext == "jpeg" or ext =="png" or ext =="jpg"):
                aname = user_filename.split('.')[0]
                filename = '{}.{}'.format(aname,ext)
                pathname = os.path.join('/home/sjin/multiplicity/uploads',filename)
                print(pathname)
                print('before save')
                pic.save(pathname)
                print('after save')
                print(pic)
                conn = lookup.getConn('sjin$sjin')
                curs = dbo.dictCursor(conn)
                insertSuccessful = lookup.updateMemberPic(conn, id, name, orgMail, password, bio, link, cell, filename)

                if (insertSuccessful):
                    curs.execute('insert into noti (orgid, unchecked) values (%s, %s)', [id, 0])
                    flash("Successfully registered new organization " + name)
                else:
                    flash("Error registering")
                conn.close()
                return redirect(url_for("main"))
            else:
                flash('Incorrect format for picture. Please upload .jpeg, .png, or .jpg.')
                conn.close()
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
        conn = lookup.getConn('sjin$sjin')
        curs = dbo.dictCursor(conn)
        curs.execute("SELECT orgMail,password FROM member WHERE orgMail = %s",[username])
        row = curs.fetchone()
        conn.close()
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
            conn = lookup.getConn('sjin$sjin')
            curs = dbo.dictCursor(conn)
            curs.execute("SELECT * FROM member WHERE orgMail = %s",[username])
            row = curs.fetchone()
            conn.close()
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
    conn = lookup.getConn('sjin$sjin')
    curs = dbo.dictCursor(conn)
    curs.execute('delete from log where orgid=%s', [id])
    curs.execute('insert into log (orgid) values (%s)', [id])
    conn.close()
    flash('You are now logged out.')
    return redirect( url_for('main') )


@app.route('/home/<id>/')
def home(id):
    conn = lookup.getConn('sjin$sjin')
    curs = dbo.dictCursor(conn)
    curs.execute('select * from member where orgid=%s', [id])
    orgInfo = curs.fetchone()
    orgname=orgInfo['name']

    curs.execute('select * from noti where orgid=%s', [id])
    noti = curs.fetchone()
    notitime=noti['postedat']
    curs.execute('select * from collab where vorgid=%s AND postedat>= %s', [id, notitime])
    collabsss = curs.fetchall()
    ccnum=len(collabsss)
    curs.execute('select * from rsvps where orgid=%s AND postedat>= %s', [id, notitime])
    eventssss = curs.fetchall()
    eenum=len(eventssss)
    unchecked = ccnum + eenum
    curs.execute('update noti set unchecked = %s where orgid = %s', [unchecked, id])


    curs.execute('select * from staff where orgid=%s', [id])
    sInfo = curs.fetchall()
    curs.execute('select postedat from log where orgid=%s', [id])
    a = curs.fetchone()
    if (a):
        time=a['postedat']
        print("this is time")
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
        conn.close()
    else:
        curs.execute('select * from collab where vorgid=%s', [id])
        newcollab = curs.fetchall()
        newevents=[]
        newposts=[]
        cnum=0
        pnum=0
        enum=0
        conn.close()
    return render_template('myhome.html', unchecked = unchecked, data = orgInfo, staff_data = sInfo, new=newcollab, events=newevents, posts=newposts, cnum=cnum, enum=enum, pnum=pnum )

@app.route('/myProfile/<id>')
def myProfile(id):
    conn = lookup.getConn('sjin$sjin')
    curs = dbo.dictCursor(conn)
    curs.execute('select * from member where orgid=%s', [id])
    orgInfo = curs.fetchone()
    curs.execute('select * from staff where orgid=%s', [id])
    sInfo = curs.fetchall()

    curs.execute('select * from noti where orgid=%s', [id])
    noti = curs.fetchone()
    notitime=noti['postedat']
    curs.execute('select * from collab where vorgid=%s AND postedat>= %s', [id, notitime])
    collabsss = curs.fetchall()
    ccnum=len(collabsss)
    curs.execute('select * from rsvps where orgid=%s AND postedat>= %s', [id, notitime])
    eventssss = curs.fetchall()
    eenum=len(eventssss)
    unchecked = ccnum + eenum
    curs.execute('update noti set unchecked = %s where orgid = %s', [unchecked, id])

    conn.close()
    return render_template('myProfile.html', unchecked = unchecked, data = orgInfo, staff_data = sInfo)

@app.route('/myEvents/<id>')
def myEvents(id):
    conn = lookup.getConn('sjin$sjin')
    curs = dbo.dictCursor(conn)
    curs.execute('select * from member where orgid=%s', [id])
    orgInfo = curs.fetchone()
    curs.execute('select * from events where orgid=%s', [id])
    events = curs.fetchall()

    curs.execute('select * from noti where orgid=%s', [id])
    noti = curs.fetchone()
    notitime=noti['postedat']
    curs.execute('select * from collab where vorgid=%s AND postedat>= %s', [id, notitime])
    collabsss = curs.fetchall()
    ccnum=len(collabsss)
    curs.execute('select * from rsvps where orgid=%s AND postedat>= %s', [id, notitime])
    eventssss = curs.fetchall()
    eenum=len(eventssss)
    unchecked = ccnum + eenum
    curs.execute('update noti set unchecked = %s where orgid = %s', [unchecked, id])
    conn.close()
    return render_template('myEvents.html', unchecked = unchecked, data = orgInfo,  events = events)

@app.route('/devent/<eid>/', methods=['GET','POST'])
def devent(eid):
    conn = lookup.getConn('sjin$sjin')
    curs = dbo.dictCursor(conn)
    curs.execute('select * from events where eid = %s', [eid])
    event = curs.fetchone()
    orgid = event['orgid']
    curs.execute('delete from events where eid = %s', [eid])
    flash("event was deleted successfully.")
    conn.close()
    return redirect(url_for('myEvents', id = orgid ))

@app.route('/aboutEvent/<id>/<eid>')
def aboutEvent(id, eid):
    conn = lookup.getConn('sjin$sjin')
    curs = dbo.dictCursor(conn)
    curs.execute('select * from member where orgid=%s', [id])
    orgInfo = curs.fetchone()
    curs.execute('select * from events where eid=%s', [eid])
    event = curs.fetchone()
    curs.execute('select * from rsvps where eid=%s', [eid])
    rsvps = curs.fetchall()
    curs.execute('select * from noti where orgid=%s', [id])
    noti = curs.fetchone()
    notitime=noti['postedat']
    curs.execute('select * from collab where vorgid=%s AND postedat>= %s', [id, notitime])
    collabsss = curs.fetchall()
    ccnum=len(collabsss)
    curs.execute('select * from rsvps where orgid=%s AND postedat>= %s', [id, notitime])
    eventssss = curs.fetchall()
    eenum=len(eventssss)
    unchecked = ccnum + eenum
    curs.execute('update noti set unchecked = %s where orgid = %s', [unchecked, id])
    conn.close()
    return render_template('aboutEvent.html', unchecked = unchecked, data = orgInfo,  event = event, rsvps = rsvps)

@app.route('/pic/<id>')
def pic(id):
    conn = lookup.getConn('sjin$sjin')
    curs = dbo.dictCursor(conn)
    curs.execute('select pic from member where orgid = %s', [id])
    row = curs.fetchone()
    conn.close()
    resp = make_response(send_from_directory('/home/sjin/multiplicity/uploads',row['pic']))
    resp.headers['Cache-Control'] = 'no-cache'
    return resp

@app.route('/spic/<sid>')
def spic(sid):
    conn = lookup.getConn('sjin$sjin')
    curs = dbo.dictCursor(conn)
    curs.execute('select pic from staff where sid = %s', [sid])
    row = curs.fetchone()
    conn.close()
    return send_from_directory('/home/sjin/multiplicity/uploads',row['pic'])


@app.route('/crequest/<id>')
def crequest(id):
    conn = lookup.getConn('sjin$sjin')
    curs = dbo.dictCursor(conn)

    curs.execute('select * from member where orgid=%s', [id])
    orgInfo = curs.fetchone()
    curs.execute('select * from collab where orgid=%s order by postedat DESC', [id])
    sends = curs.fetchall()
    snum=len(sends)
    curs.execute('select * from collab where vorgid=%s order by postedat DESC', [id])
    receives = curs.fetchall()
    rnum=len(receives)
    curs.execute('select * from noti where orgid=%s', [id])
    noti = curs.fetchone()
    notitime=noti['postedat']
    curs.execute('select * from collab where vorgid=%s AND postedat>= %s', [id, notitime])
    collabsss = curs.fetchall()
    ccnum=len(collabsss)
    curs.execute('select * from rsvps where orgid=%s AND postedat>= %s', [id, notitime])
    eventssss = curs.fetchall()
    eenum=len(eventssss)
    unchecked = ccnum + eenum
    curs.execute('update noti set unchecked = %s where orgid = %s', [unchecked, id])
    conn.close()
    return render_template('crequest.html', unchecked = unchecked, data = orgInfo,  sends = sends, receives = receives, snum=snum, rnum=rnum)


@app.route('/noti/<id>/')
def noti(id):
    conn = lookup.getConn('sjin$sjin')
    curs = dbo.dictCursor(conn)


    curs.execute('select * from member where orgid=%s', [id])
    orgInfo = curs.fetchone()

    curs.execute('select * from noti where orgid=%s', [id])
    noti = curs.fetchone()
    unchecked = noti['unchecked']
    if (unchecked == 0):
        newcollab = []
        newrsvps=[]

        cnum=0
        rnum=0

        curs.execute('delete from noti where orgid=%s', [id])
        curs.execute('insert into noti (orgid, unchecked) values (%s, %s)', [id, 0])
        conn.close()
    else:
        time=noti['postedat']
        curs.execute('select * from collab where vorgid=%s AND postedat>= %s order by postedat DESC', [id, time])
        newcollab = curs.fetchall()
        cnum=len(newcollab)
        curs.execute('select * from rsvps where orgid=%s AND postedat>= %s order by postedat DESC', [id, time])
        newrsvps = curs.fetchall()
        rnum=len(newrsvps)

        curs.execute('delete from noti where orgid=%s', [id])
        curs.execute('insert into noti (orgid, unchecked) values (%s, %s)', [id, 0])
        conn.close()

    return render_template('noti.html', unchecked = unchecked, data = orgInfo, new=newcollab, rsvps = newrsvps, cnum=cnum, rnum = rnum )




@app.route('/update/<id>', methods=["GET", "POST"])
def update(id):
    conn = lookup.getConn('sjin$sjin')
    curs = dbo.dictCursor(conn)
    curs.execute('select * from member where orgid=%s', [id])
    orgInfo = curs.fetchone()
    curs.execute('select * from noti where orgid=%s', [id])
    noti = curs.fetchone()
    notitime=noti['postedat']
    curs.execute('select * from collab where vorgid=%s AND postedat>= %s', [id, notitime])
    collabsss = curs.fetchall()
    ccnum=len(collabsss)
    curs.execute('select * from rsvps where orgid=%s AND postedat>= %s', [id, notitime])
    eventssss = curs.fetchall()
    eenum=len(eventssss)
    unchecked = ccnum + eenum
    curs.execute('update noti set unchecked = %s where orgid = %s', [unchecked, id])
    if request.method=="GET":
        conn.close()
        return render_template('update.html', unchecked = unchecked, data=orgInfo)
    else:
        name=request.form['name']
        orgMail=request.form['orgMail']
        password=request.form['password']
        bio=request.form['bio']
        link=request.form['link']
        cell=request.form['cell']
        pcheck=request.form['pcheck']

        if (password == pcheck):
            pic = request.files['pic']
            print('original pic')
            print(pic)
            user_filename = pic.filename
            ext = user_filename.split('.')[-1]
            aname = user_filename.split('.')[0]
            filename = '{}.{}'.format(aname,ext)
            print(filename)
            if (filename=="."):
                insertSuccessful = lookup.updateMember(conn, id, name, orgMail, password, bio, link, cell)
                if (insertSuccessful):
                    flash("Successfully updated org " + name)
                else:
                    flash("Error updating")
                conn.close()
                return redirect(url_for("myProfile", id = id))
            else:
                if (ext == "jpeg" or ext =="png" or ext =="jpg"):
                    pathname = os.path.join('/home/sjin/multiplicity/uploads',filename)
                    print(pathname)
                    print('here pic')
                    pic.save(pathname)

                    print(pic)
                    insertSuccessful = lookup.updateMemberPic(conn, id, name, orgMail, password, bio, link, cell, filename)
                    if (insertSuccessful):
                        flash("Successfully updated org " + name)
                    else:
                        flash("Error updating")
                    conn.close()
                    return redirect(url_for("myProfile", id = id))
                else:
                    flash('Incorrect format for picture. Please upload .jpeg, .png, or .jpg.')
                    return render_template('update.html', unchecked = unchecked, data=orgInfo)


        else:
            flash("Password does not match.")
            return render_template('update.html', unchecked = unchecked, data=orgInfo)


@app.route('/addStaff/<id>/', methods=['GET','POST'])
def addStaff(id):
    conn = lookup.getConn('sjin$sjin')
    curs = dbo.dictCursor(conn)
    curs.execute('select * from member where orgid=%s', [id])
    orgInfo = curs.fetchone()
    curs.execute('select * from noti where orgid=%s', [id])
    noti = curs.fetchone()
    notitime=noti['postedat']
    curs.execute('select * from collab where vorgid=%s AND postedat>= %s', [id, notitime])
    collabsss = curs.fetchall()
    ccnum=len(collabsss)
    curs.execute('select * from rsvps where orgid=%s AND postedat>= %s', [id, notitime])
    eventssss = curs.fetchall()
    eenum=len(eventssss)
    unchecked = ccnum + eenum
    curs.execute('update noti set unchecked = %s where orgid = %s', [unchecked, id])
    if request.method == 'GET':
        conn.close()
        return render_template('addStaff.html', unchecked = unchecked, data=orgInfo)
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
        pathname = os.path.join('/home/sjin/multiplicity/uploads',filename)
        pic.save(pathname)
        conn = lookup.getConn('sjin$sjin')
        insertSuccessful = lookup.addStaff(conn, orgid, sName, sEmail, sTitle, filename)
        if (insertSuccessful):
            conn.close()
            flash("Successfully added a new staff " + sName)
        else:
            conn.close()
            flash("Error adding staff")
        return redirect(url_for("myProfile", id = id))

@app.route('/dstaff/<sid>/', methods=['GET','POST'])
def dstaff(sid):
    conn = lookup.getConn('sjin$sjin')
    curs = dbo.dictCursor(conn)
    curs.execute('delete from staff where sid = %s', [sid])
    flash("staff was deleted successfully.")
    conn.close()
    return redirect(request.referrer)


@app.route('/dcollab/<cid>/', methods=['GET','POST'])
def dcollab(cid):
    conn = lookup.getConn('sjin$sjin')
    curs = dbo.dictCursor(conn)
    curs.execute('delete from collab where collabid = %s', [cid])
    flash("Collab Request was deleted successfully. The receiver will no longer see your collab request.")
    conn.close()
    return redirect(request.referrer)

@app.route('/dpost/<pid>/', methods=['GET','POST'])
def dpost(pid):
    conn = lookup.getConn('sjin$sjin')
    curs = dbo.dictCursor(conn)
    curs.execute('delete from post where pid = %s', [pid])
    flash("post was deleted successfully.")
    conn.close()
    return redirect(request.referrer)


@app.route('/singleP/<id>/<vid>')
def singleP(id, vid):
    conn = lookup.getConn('sjin$sjin')
    curs = dbo.dictCursor(conn)
    curs.execute('select * from member where orgid=%s', [id])
    orgInfo = curs.fetchone()
    curs.execute('select * from member where orgid=%s', [vid])
    vorgInfo = curs.fetchone()
    curs.execute('select * from staff where orgid=%s', [vid])
    sInfo = curs.fetchall()
    curs.execute('select * from noti where orgid=%s', [id])
    noti = curs.fetchone()
    notitime=noti['postedat']
    curs.execute('select * from collab where vorgid=%s AND postedat>= %s', [id, notitime])
    collabsss = curs.fetchall()
    ccnum=len(collabsss)
    curs.execute('select * from rsvps where orgid=%s AND postedat>= %s', [id, notitime])
    eventssss = curs.fetchall()
    eenum=len(eventssss)
    unchecked = ccnum + eenum
    curs.execute('update noti set unchecked = %s where orgid = %s', [unchecked, id])
    conn.close()
    return render_template('singleP.html', unchecked = unchecked, data = orgInfo, vdata = vorgInfo, staff_data = sInfo)

@app.route('/collab/<id>/<vid>', methods=['GET','POST'])
def collab(id, vid):
    conn = lookup.getConn('sjin$sjin')
    curs = dbo.dictCursor(conn)
    curs.execute('select * from member where orgid=%s', [id])
    orgInfo = curs.fetchone()
    curs.execute('select * from member where orgid=%s', [vid])
    vorgInfo = curs.fetchone()
    curs.execute('select * from noti where orgid=%s', [id])
    noti = curs.fetchone()
    notitime=noti['postedat']
    curs.execute('select * from collab where vorgid=%s AND postedat>= %s', [id, notitime])
    collabsss = curs.fetchall()
    ccnum=len(collabsss)
    curs.execute('select * from rsvps where orgid=%s AND postedat>= %s', [id, notitime])
    eventssss = curs.fetchall()
    eenum=len(eventssss)
    unchecked = ccnum + eenum
    curs.execute('update noti set unchecked = %s where orgid = %s', [unchecked, id])
    if request.method == 'GET':
        conn.close()
        return render_template('collab.html', unchecked = unchecked, data = orgInfo, vdata = vorgInfo)
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
        accepted = None
        conn = lookup.getConn('sjin$sjin')
        insertSuccessful = lookup.collab(conn, orgid, sName, vorgid, rName, msg, accepted)
        if (insertSuccessful):
            conn.close()
            flash("Successfully sent collab request to " + rName)
        else:
            conn.close()
            flash("Error sending request")
        return redirect(url_for("members", id = id))

@app.route('/confirm/<cid>', methods=['GET','POST'])
def confirm(cid):
    conn = lookup.getConn('sjin$sjin')
    curs = dbo.dictCursor(conn)
    status = "Confirmed"
    curs.execute('update collab set accepted = %s where collabid = %s', [status, cid])
    flash("Collab Request confirmed.")
    conn.close()
    return redirect(request.referrer)

@app.route('/reject/<cid>', methods=['GET','POST'])
def reject(cid):
    conn = lookup.getConn('sjin$sjin')
    curs = dbo.dictCursor(conn)
    status = "Rejected"
    curs.execute('update collab set accepted = %s where collabid = %s', [status, cid])
    flash("Collab Request rejected.")
    conn.close()
    return redirect(request.referrer)


@app.route('/rsvp/<id>', methods=['GET','POST'])
def rsvp(id):
    eid = request.form['eid']
    conn = lookup.getConn('sjin$sjin')
    curs = dbo.dictCursor(conn)

    curs.execute('select * from member where orgid=%s', [id])
    orgInfo = curs.fetchone()
    name = orgInfo['name']
    curs.execute('select * from events where eid=%s', [eid])
    eInfo = curs.fetchone()

    postedat = eInfo['postedat']
    eName = eInfo['eName']
    orgid = eInfo['orgid']
    orgName = eInfo['orgName']
    eDate=eInfo['eDate']
    eTime=eInfo['eTime']
    location=eInfo['location']
    address1=eInfo['address1']
    address2=eInfo['address2']
    eState=eInfo['eState']
    eZip=eInfo['eZip']
    eBio=eInfo['eBio']
    rsvp=eInfo['rsvp']
    people = request.form['num']
    num = int(people)
    new = rsvp + num
    print('here')
    print(new)
    curs.execute('insert into events values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) ON DUPLICATE KEY UPDATE rsvp=%s', [eid, postedat, eName, orgid, orgName, eDate, eTime, location, address1, address2, eState, eZip, eBio, new, new])
    curs.execute('insert into rsvps (eid, eName, orgName, rsvp, orgid) values (%s, %s, %s, %s, %s)', [eid, eName, name, num, orgid])

    conn.close()
    return jsonify({'error': False, 'eid': eid, 'num': new})


@app.route('/resources/<id>/')
def resources(id):
    conn = lookup.getConn('sjin$sjin')
    curs = dbo.dictCursor(conn)
    curs.execute('select * from member where orgid=%s', [id])
    orgInfo = curs.fetchone()
    curs.execute('select * from noti where orgid=%s', [id])
    noti = curs.fetchone()
    notitime=noti['postedat']
    curs.execute('select * from collab where vorgid=%s AND postedat>= %s', [id, notitime])
    collabsss = curs.fetchall()
    ccnum=len(collabsss)
    curs.execute('select * from rsvps where orgid=%s AND postedat>= %s', [id, notitime])
    eventssss = curs.fetchall()
    eenum=len(eventssss)
    unchecked = ccnum + eenum
    curs.execute('update noti set unchecked = %s where orgid = %s', [unchecked, id])
    conn.close()
    return render_template('resources.html', unchecked = unchecked, data = orgInfo)


#member table and search bar
@app.route('/member/<id>/',methods=["GET","POST"])
@app.route('/member/<id>/<ask>', methods=["GET","POST"])
def members(id, ask=None):
    conn = lookup.getConn('sjin$sjin')
    curs = dbo.dictCursor(conn)
    curs.execute('select * from member where orgid=%s', [id])
    orgInfo = curs.fetchone()
    curs.execute('select * from noti where orgid=%s', [id])
    noti = curs.fetchone()
    notitime=noti['postedat']
    curs.execute('select * from collab where vorgid=%s AND postedat>= %s', [id, notitime])
    collabsss = curs.fetchall()
    ccnum=len(collabsss)
    curs.execute('select * from rsvps where orgid=%s AND postedat>= %s', [id, notitime])
    eventssss = curs.fetchall()
    eenum=len(eventssss)
    unchecked = ccnum + eenum
    curs.execute('update noti set unchecked = %s where orgid = %s', [unchecked, id])
    if request.method == 'POST':
        ask = request.form['search-name']
        conn.close()
        return redirect(url_for('members', ask=ask, id=orgInfo['orgid']))
    else:
        if ask == None:
            member = lookup.getAllMembers(conn)
        else:
            member = lookup.getMembers(conn, ask)
        conn.close()
        return render_template('member.html',
                                member_data=member, orgInfo=orgInfo, data = orgInfo, unchecked = unchecked)

@app.route('/events/<id>/',methods=["GET","POST"])
@app.route('/events/<id>/<ask1>/', methods=["GET","POST"])
@app.route('/events/<id>/<ask1>/<ask2>', methods=["GET","POST"])
def events(id, ask1=None, ask2=None):
    conn = lookup.getConn('sjin$sjin')
    curs = dbo.dictCursor(conn)
    curs.execute('select * from member where orgid=%s', [id])
    orgInfo = curs.fetchone()
    curs.execute('select * from noti where orgid=%s', [id])
    noti = curs.fetchone()
    notitime=noti['postedat']
    curs.execute('select * from collab where vorgid=%s AND postedat>= %s', [id, notitime])
    collabsss = curs.fetchall()
    ccnum=len(collabsss)
    curs.execute('select * from rsvps where orgid=%s AND postedat>= %s', [id, notitime])
    eventssss = curs.fetchall()
    eenum=len(eventssss)
    unchecked = ccnum + eenum
    curs.execute('update noti set unchecked = %s where orgid = %s', [unchecked, id])
    if request.method == 'POST':
        ask1 = request.form['search-event']
        if(ask1):
            print(ask1)
            conn.close()
            return redirect(url_for('events', ask1=ask1, ask2=None, id=orgInfo['orgid']))
        else:
            ask1 = request.form['start-date']
            ask2 = request.form['end-date']
            conn.close()
            return redirect(url_for('events', ask1=ask1,  ask2=ask2, id=orgInfo['orgid']))
    else:
        if ask1 == None:
            events = lookup.getAllEvents(conn)
        else:
            if ask2 == None:
                events = lookup.getEvents(conn, ask1, ask2)
            else:
                events = lookup.getDateEvents(conn, ask1, ask2)
        conn.close()
        return render_template('events.html', unchecked = unchecked,
                                events_data=events, orgInfo=orgInfo, data = orgInfo)


@app.route('/singleEvent/<id>/<eid>', methods=['GET','POST'])
def singleEvent(id, eid):
    conn = lookup.getConn('sjin$sjin')
    curs = dbo.dictCursor(conn)
    curs.execute('select * from member where orgid=%s', [id])
    orgInfo = curs.fetchone()
    curs.execute('select * from events where eid=%s', [eid])
    eventData = curs.fetchone()
    curs.execute('select * from noti where orgid=%s', [id])
    noti = curs.fetchone()
    notitime=noti['postedat']
    curs.execute('select * from collab where vorgid=%s AND postedat>= %s', [id, notitime])
    collabsss = curs.fetchall()
    ccnum=len(collabsss)
    curs.execute('select * from rsvps where orgid=%s AND postedat>= %s', [id, notitime])
    eventssss = curs.fetchall()
    eenum=len(eventssss)
    unchecked = ccnum + eenum
    curs.execute('update noti set unchecked = %s where orgid = %s', [unchecked, id])
    return render_template('singleEvent.html',
                                unchecked = unchecked, edata = eventData, orgInfo=orgInfo, data = orgInfo)




@app.route('/createEvents/<id>/', methods=['GET','POST'])
def createEvents(id):
    conn = lookup.getConn('sjin$sjin')
    curs = dbo.dictCursor(conn)
    curs.execute('select * from member where orgid=%s', [id])
    orgInfo = curs.fetchone()
    curs.execute('select * from noti where orgid=%s', [id])
    noti = curs.fetchone()
    notitime=noti['postedat']
    curs.execute('select * from collab where vorgid=%s AND postedat>= %s', [id, notitime])
    collabsss = curs.fetchall()
    ccnum=len(collabsss)
    curs.execute('select * from rsvps where orgid=%s AND postedat>= %s', [id, notitime])
    eventssss = curs.fetchall()
    eenum=len(eventssss)
    unchecked = ccnum + eenum
    curs.execute('update noti set unchecked = %s where orgid = %s', [unchecked, id])
    if request.method == 'GET':
        conn.close()
        return render_template('createEvents.html', unchecked = unchecked, data=orgInfo)
    elif request.method == 'POST':
        eName=request.form['eName']
        orgid = id
        orgName = orgInfo['name']
        eDate=request.form['eDate']
        eTime=request.form['eTime']
        location=request.form['location']
        address1 = request.form['address1']
        address2 = request.form['address2']
        eState = request.form['state']
        eZip = request.form['zip']
        eBio=request.form['eBio']
        conn = lookup.getConn('sjin$sjin')
        insertSuccessful = lookup.insertEvents(conn, eName, orgid, orgName, eDate, eTime, location, address1, address2, eState, eZip, eBio)
        if (insertSuccessful):
            flash("Successfully created a new event: [" + eName + "]")
        else:
            flash("Error creating events")
        conn.close()
        return redirect(url_for("events", id = id))


#private forum page
@app.route('/pforum/<id>/')
def pforum(id):
    conn = lookup.getConn('sjin$sjin')
    curs = dbo.dictCursor(conn)
    curs.execute('select * from member where orgid=%s', [id])
    orgInfo = curs.fetchone()
    username = orgInfo['name']
    posts = lookup.getAllPosts(conn)
    curs.execute('select * from noti where orgid=%s', [id])
    noti = curs.fetchone()
    notitime=noti['postedat']
    curs.execute('select * from collab where vorgid=%s AND postedat>= %s', [id, notitime])
    collabsss = curs.fetchall()
    ccnum=len(collabsss)
    curs.execute('select * from rsvps where orgid=%s AND postedat>= %s', [id, notitime])
    eventssss = curs.fetchall()
    eenum=len(eventssss)
    unchecked = ccnum + eenum
    curs.execute('update noti set unchecked = %s where orgid = %s', [unchecked, id])
    conn.close()
    return render_template('privateForum.html',
                            unchecked = unchecked, post_data=posts, data=orgInfo, username = username)


#insert a post on private page
@app.route('/ppost/<id>/', methods=['GET','POST'])
def ppost(id):
    conn = lookup.getConn('sjin$sjin')
    curs = dbo.dictCursor(conn)
    curs.execute('select * from member where orgid=%s', [id])
    orgInfo = curs.fetchone()
    curs.execute('select * from noti where orgid=%s', [id])
    noti = curs.fetchone()
    notitime=noti['postedat']
    curs.execute('select * from collab where vorgid=%s AND postedat>= %s', [id, notitime])
    collabsss = curs.fetchall()
    ccnum=len(collabsss)
    curs.execute('select * from rsvps where orgid=%s AND postedat>= %s', [id, notitime])
    eventssss = curs.fetchall()
    eenum=len(eventssss)
    unchecked = ccnum + eenum
    curs.execute('update noti set unchecked = %s where orgid = %s', [unchecked, id])
    if request.method == 'GET':
        conn.close()
        return render_template('insertPPost.html', unchecked = unchecked, data = orgInfo)
    elif request.method == 'POST':
        now = datetime.now()
        postedat = now.strftime("%d/%m/%Y %H:%M:%S")
        poster=orgInfo['name']
        theme=request.form['theme']
        thing=request.form['thing']
        conn = lookup.getConn('sjin$sjin')
        insertSuccessful = lookup.insertPost(conn, postedat, poster, theme, thing)
        if (insertSuccessful):
            print("posted by " + poster)
            flash("Successfully posted "+ theme)
        else:
            flash("Error")
        conn.close()
        return redirect(url_for("pforum", id=id))

#ajax route for comments
@app.route('/commentAjax/', methods=['GET','POST'])
def commentAjax():
     if request.method == 'GET':
        #getting the id of the post
        postid = request.args['postid']
        conn = getConn('sjin$sjin')
        curs = dbo.dictCursor(conn)
        #getting all the comments with the postid from the comment database
        curs.execute("SELECT commentid, content FROM comment WHERE postid = %s",[postid])
        matches = curs.fetchall()
        conn.close()
        return jsonify({'error': False, 'postid': postid, 'matches': matches})
     else:
        #getting postid and comment from the request form
        postid = request.form['cu']
        comment = request.form['comment']
        conn = getConn('sjin$sjin')
        curs = dbo.dictCursor(conn)
        #store the comment in the comment table
        curs.execute('insert into comment (postid, content) values (%s, %s)', [postid, comment])
        conn.close()
        return jsonify({'error': False, 'postid': postid, 'comment': comment})



if __name__ == '__main__':
    import os
    uid = "1234"
    app.debug = True
    app.run('0.0.0.0',uid)

