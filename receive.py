from flask import Flask, render_template
from twilio.rest import Client
from flask_sqlalchemy import SQLAlchemy
from config import DATABASE_URL, SECRET_KEY

app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
db = SQLAlchemy(app)


@app.route("/sms", methods=['POST'], ['GET'])
def sms_receive():
    receive_number = request.form['From']
    receive_body = request.form['body']
    add = add(receive_number, receive_body)


# class for database model
class receiveInfo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    receive_message = db.Column(db.String)
    receive_number = db.Column(db.BigInteger)


# add to database and commit
def add(message, number):
    receive_info = receiveInfo(receive_message=message, receive_number=number)
    db.session.add(receive_info)
    db.session.commit()


if __name__ == '__main__':
    app.run(debug=True)
