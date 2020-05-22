from flask import Flask
from flask_mail import Mail, Message

app = Flask(__name__)
app.config.update(
	DEBUG=True,
	#EMAIL SETTINGS
	MAIL_SERVER='smtp.gmail.com',
	MAIL_PORT=465,
	MAIL_USE_SSL=True,
	MAIL_USERNAME = 'christinejin9@gmail.com',
	MAIL_PASSWORD = '8hZ47vU3'
	)
mail = Mail(app)

@app.route('/send-mail/')
def send_mail():
		msg = Message("Send Mail Tutorial!",
		  sender="christinejin9@gmail.com",
		  recipients=["sjin@wellesley.edu"])
		msg.body = "the prince is doing fine he just need 10M dollars to escape to Germany"           
		mail.send(msg)
		return 'Mail sent!'



if __name__ == '__main__':
    import os
    uid = "1998"
    app.debug = True
    app.run('0.0.0.0',uid)
