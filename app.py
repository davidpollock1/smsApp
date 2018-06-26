from flask import Flask, render_template, flash, request, redirect
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField
from wtforms.widgets import TextArea
from twilio.rest import Client
from flask_sqlalchemy import SQLAlchemy
from config import account_sid, auth_token

from twilio.twiml.messaging_response import MessagingResponse



app = Flask(__name__)
app.config['SECRET_KEY'] = 'super-secret-key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:@localhost/learningflask'
db = SQLAlchemy(app)


# if form validates, calls to send_sms function and adds to database
@app.route('/form', methods=['GET', 'POST'])
def form():
	form = sendForm()
	if form.validate_on_submit():
		results = send_sms(form.message.data, form.contactNum.data)
		addDB = add(form.message.data, form.contactNum.data)
	return render_template('form.html', form=form)


@app.route("/sms", methods=['GET', 'POST'])
def sms_reply():
    """Respond to incoming texts with message"""
    # Start our TwiML response
    resp = MessagingResponse()

    # Add a message
    resp.message("Thank you for contacting Land Title")

    return str(resp)


# class for database model
class smsInfo(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	message = db.Column(db.String)
	contactNum = db.Column(db.BigInteger)



# add to database and commit
def add(message,contactNum):
	info = smsInfo(message=message,contactNum=contactNum) #testing 
	db.session.add(info)
	db.session.commit()



# wtform web form
class sendForm(FlaskForm):
	message = StringField('Message', widget=TextArea())
	contactNum = IntegerField('Contact Number')



# function that actually sends message
def send_sms(message, contactNum):
	client = Client(account_sid, auth_token)
	return client.messages.create(
                            to=contactNum,
                            body=message,
                            from_='12486174847')



if __name__ == '__main__':
	app.run(debug=True)