from flask import Flask,render_template,request, jsonify, make_response, session, flash, redirect
import boto3
import uuid
from boto3 import Session
from boto3.dynamodb.conditions import Key,Attr
import os
import numpy as np
import pickle as p 
import json
import random

app=Flask(__name__)
app.secret_key=os.urandom(24)

session = Session()
credentials = session.get_credentials()
current_credentials = credentials.get_frozen_credentials()
dynamodb = boto3.resource('dynamodb',
aws_access_key_id=current_credentials.access_key,
aws_secret_access_key=current_credentials.secret_key)

# IMPORTANT: these strings will be replaced with the user's input on the form later, i put the column names here to show the order the 
allFormDetails = [
    "case_id", 
    "hospital_code", 
    "hospital_type_code",
    "city_code_hospital",
    "hospital_region_code", 
    "available_extra_rooms", 
    "department", 
    "ward_type", 
    "ward_facility_code",
    "bed_grade",
    "type_of_admission", 
    "severity_of_illness", 
    "no_of_visits", 
    "age_range",
    "admission_deposit"
]
modelInput = []  # must append allFormDetails array into another array to feed to model

@app.route('/')
def login():
    return render_template('register.html')

@app.route('/register', methods=['POST'])
def register():
    if request.method == 'POST':
        spot_id = uuid.uuid4() #Unique identifier for spot
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        email=request.form.get('email')
        password=request.form.get('password')
        print(first_name,last_name,email)
        table = dynamodb.Table('user_auth')
        table.put_item(
        Item={  'uuid': str(spot_id),
                'email': email,
                'first_name': first_name,
                'last_name': last_name,
                'password':password
            }
        )
        msg = "Registration Complete. Please Login to your account !"
        return render_template('register.html',msg=msg)
    return render_template('register.html',msg="Registration Complete. Please Login to your account !")
    

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

        # retrieve data from form
        patientDetails = request.form
        age_range = patientDetails['age_range']
        admission_type = patientDetails['admission_type']
        illness_severity = patientDetails['illness_severity']
        department = patientDetails['department']
        no_of_visits = patientDetails['no_of_visitors']
        admission_deposit = patientDetails['admission_deposit']
        print("patient details: ", patientDetails)

        # append values into array via its index
        allFormDetails[6] = department
        allFormDetails[10] = admission_type
        allFormDetails[11] = illness_severity
        allFormDetails[12] = no_of_visits
        allFormDetails[13] = age_range
        allFormDetails[14] = admission_deposit
        print("patient - allFormDetails: ", allFormDetails)
        return redirect('/estimate_stay')
    return render_template('register_patient.html')

@app.route('/book_appointments')
def book_appointments():
    return render_template('book_appointments.html')

@app.route('/settings')
def settings():
    return render_template('settings.html')

@app.route('/login', methods=['GET','POST'])
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
    else:
        return render_template('login.html',msg="")

@app.route('/estimate_stay', methods=['GET', 'POST'])
def estimate_stay():
    hospitalDetails = "none"
    if request.method == 'POST':
        # hospitalDetails = request.form.to_dict()  # converts ImmutableMultiDict to JSON object
        
        # generate random caseID
        caseID = random.randint(0, 20)

        # retrieve data from form
        hospitalDetails = request.form
        h_code = hospitalDetails['h_code']
        ht_code = hospitalDetails['ht_code']
        hc_code = hospitalDetails['hc_code']
        hr_code = hospitalDetails['hr_code']
        room_availability = hospitalDetails['room_availability']
        ward_type = hospitalDetails['ward_type']
        ward_facility = hospitalDetails['ward_facility']
        bed_grade = hospitalDetails['bed_grade']
        print("hospital details: ", request.form)

        allFormDetails[0] = str(caseID)
        allFormDetails[1] = h_code
        allFormDetails[2] = ht_code
        allFormDetails[3] = hc_code
        allFormDetails[4] = hr_code
        allFormDetails[5] = room_availability
        allFormDetails[7] = ward_type
        allFormDetails[8] = ward_facility
        allFormDetails[9] = bed_grade
        print("all details: ", allFormDetails)

        # calculate LoS
        makecalc()
    return render_template('estimate_stay.html')

def strToFloat(array): 
    for i in array: 
        i = int(float(i))
    print("float array: ", array)
    return array
    
@app.route('/api/', methods=['POST'])
def makecalc():
    modelfile = './final_prediction.pickle'
    model = p.load(open(modelfile, 'rb'))
    print("allDetails: ", allFormDetails)
    modelInput.append(allFormDetails)
    print("model input: ", modelInput)
    prediction = np.array2string(model.predict(modelInput))
    print("prediction for random data: ", prediction)
    return jsonify(prediction)

if __name__ == "__main__":
    app.run(debug=True)
   

   # flask with ML
   #https://www.youtube.com/watch?v=UbCWoMf80PY&feature=emb_logo
