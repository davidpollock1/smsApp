from flask import Flask, render_template,
from twilio.rest import Client
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
db = SQLAlchemy(app)

@app.route("/sms", methods=['GET', 'POST'])
def sms_receive():
    receive_number = request.form['From']
    receive_body = request.form['body']

# class for database model
class receiveInfo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    receive_message = db.Column(db.String)
    receive_number = db.Column(db.BigInteger)


# add to database and commit
def add(message, number):
    info = receiveInfo(message=message, contactNum=contactNum)
    db.session.add(info)
    db.session.commit()

if __name__ == '__main__':
    app.run(debug=True)