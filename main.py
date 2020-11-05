from flask import Flask,render_template,request, jsonify, make_response, session,flash
import boto3
import uuid
from boto3 import Session
from boto3.dynamodb.conditions import Key,Attr
import os


app=Flask(__name__)
app.secret_key=os.urandom(24)


session = Session()
credentials = session.get_credentials()
current_credentials = credentials.get_frozen_credentials()
dynamodb = boto3.resource('dynamodb',
aws_access_key_id=current_credentials.access_key,
aws_secret_access_key=current_credentials.secret_key)






@app.route('/')
def login():
    return render_template('login.html')

@app.route('/register', methods=['GET','POST'])
def signup():
    spot_id = uuid.uuid4() #Unique identifier for spot
    first_name = request.form.get('first_name')
    last_name = request.form.get('last_name')
    email=request.form.get('email')
    password=request.form.get('password')
    table = dynamodb.Table('user_auth')
    table.put_item(
    Item={  'uuid': str(spot_id),
            'email': email,
            'first_name': first_name,
            'last_name': last_name,
            'password':password
        }
    )
    return render_template('home.html')

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/calendar')
def calendar():
    return render_template('calendar.html')

@app.route('/estimate_stay')
def estimate_stay():
    return render_template('estimate_stay.html')

@app.route('/book_appointments')
def book_appointments():
    return render_template('book_appointments.html')

@app.route('/settings')
def settings():
    return render_template('settings.html')

@app.route('/login_validation', methods=['GET','POST'])
def login_validation():
    if request.method == 'POST':
        email=request.form['email']
        password=request.form['password']
        table = dynamodb.Table('user_auth')
        response = table.scan(FilterExpression=Key('email').eq(email))
        #print(response)
        items=response['Items']
        #print("items",items)
        if len(items)>0:
            name=items[0]['email']       
            return render_template('home.html')
        else:
            result = {}
            result ="You don't have a account. Please click create a new account"
            return render_template('login.html',msg=result)


if __name__ == "__main__":
   app.run(debug=True)
   

   # flask with ML
   #https://www.youtube.com/watch?v=UbCWoMf80PY&feature=emb_logo
