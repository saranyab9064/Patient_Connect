from flask import Flask,render_template,request, jsonify, make_response, session, flash
import boto3
import uuid
from boto3 import Session
from boto3.dynamodb.conditions import Key,Attr
import os
import numpy as np
import pickle as p 
import json


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
def about():
    if request.method =='GET':
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
        msg = "Registration Complete. Please login to your account"
        #flash("Registration Complete. Please login to your account")
        return render_template('register.html',msg=msg)
    return render_template('login.html')

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/calendar')
def calendar():
    return render_template('calendar.html')

@app.route('/register_patient', methods=['GET','POST'])
def register_patient():
    patientDetails = "none"
    if request.method == "POST": 
        patientDetails = request.form
        print("patient details: ", patientDetails)
    return render_template('register_patient.html')


@app.route('/book_appointments')
def book_appointments():
    return render_template('book_appointments.html')

@app.route('/settings')
def settings():
    return render_template('settings.html')

@app.route('/login_validation', methods=['GET','POST'])
def login_validation():
    if request.method == 'GET':
        email=request.form['email']
        password=request.form['password']
        table = dynamodb.Table('user_auth')
        response = table.query(KeyConditionExpression=Key('email').eq(email))
        items=response['Items']
        name=items[0]['name']
        if password == items[0]['password']:
            session['user_id']=items[0][0]
            return redirect('/home')
    else:
        msg = "You don't have a account. Please click signup"
        return render_template('register.html',msg=msg)

@app.route('/estimate_stay', methods=['GET', 'POST'])
def estimate_stay():
    hospitalDetails = "none"
    if request.method == 'POST':
        hospitalDetails = request.form.to_dict()  # converts ImmutableMultiDict to JSON object
        # print("hospital details: ", request.form)
        # hospitalDetails = request.get_json()
        # print("hospital details: ", hospitalDetails)
        # length_of_stay = makecalc(hospitalDetails)
        makecalc()
        # print("LoS: ", length_of_stay)
    return render_template('estimate_stay.html')

"""
15 Features in order of array indices

caseid
hospital_code
hospital_type_code
city_code_hospital
hospital_region_code
available_extra_rooms
department
ward_type
ward_facility_code
bed_grade
patientID
city_code_patient
type_of_admission
severity_of_illness
no_of_visits
age
admission_deposit
"""

@app.route('/api/', methods=['POST'])
def makecalc():
    modelfile = './final_prediction.pickle'
    model = p.load(open(modelfile, 'rb'))
    randomData = [[12, 0, 1, 1, 20, 0, 0, 1, 1, 2, 2, 1, 0, 1, 1]]  # input must be a total of 15 features, expected format is an array of arrays  
    prediction = np.array2string(model.predict(randomData))
    # output = prediction[0]
    print("prediction for random Data: ", prediction)
    return jsonify(prediction)

if __name__ == "__main__":
    app.run(debug=True)
   

   # flask with ML
   #https://www.youtube.com/watch?v=UbCWoMf80PY&feature=emb_logo
