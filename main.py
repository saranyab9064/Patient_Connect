from flask import Flask,render_template,request, jsonify, make_response, session, flash, redirect
import boto3
import uuid
from boto3 import Session
from boto3.dynamodb.conditions import Key,Attr
from botocore.exceptions import ClientError
import os
import numpy as np
import pickle as p 
import json
import random
import requests
import math

from flask import Blueprint
from flask_paginate import Pagination, get_page_parameter

app=Flask(__name__)
app.secret_key=os.urandom(24)

session = Session()
credentials = session.get_credentials()
current_credentials = credentials.get_frozen_credentials()
dynamodb = boto3.resource('dynamodb',
aws_access_key_id=current_credentials.access_key,
aws_secret_access_key=current_credentials.secret_key)

patient_uuid = "default"
user_uuid = "default"

CARDS_PER_PAGE = 4
ROWS_PER_PAGE = 2

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
# must append allFormDetails array into another array to feed to model
modelInput = []  

@app.route('/')
def login():
    return redirect('/register')

@app.route('/test', methods=['GET','POST'])
def test():
    # appointment_times = dynamodb.Table('appointment_times')
    # apptTimes = appointment_times.scan()['Items']
    # print(appointment_times.scan()['Items'][0])
    data = {'username': 'Pang', 'site': 'stackoverflow.com'}
    return render_template('test.html', data = data)

@app.route('/register', methods=['GET','POST'])
def register():
    if request.method == 'POST':
        print("-------------Register Login-----------------")
        userDetails = request.form
        # Unique identifier for spot
        spot_id = uuid.uuid4() 
        user_uuid = spot_id # use to store in appt db
        first_name = userDetails['f_name']
        last_name = userDetails['l_name']
        email = userDetails['email']
        password = userDetails['password']
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
        msg = "Registration Complete. Please Click Login here!"
        return render_template('login.html',msg=msg)     
    return render_template('register.html',msg="Please Register if you don't have an account otherwise login !")
    
def filter_patient_details(id):
    dynamo_client = boto3.client('dynamodb')
    table = dynamodb.Table('patient_details')
    # Get patient details
    pat_details = table.scan(FilterExpression=Key('uuid').eq(id))
    res_pat = pat_details['Items']
    if len(res_pat)>0:
        #print("res_pat",res_pat,len(res_pat),res_pat[0]['first_name'])
        f_name = res_pat[0]['first_name']
        l_name= res_pat[0]['last_name']
        email_id= res_pat[0]['email']
        gender = res_pat[0]['gender']
        add_notes = res_pat[0]['additional_info']
        return(f_name,l_name,email_id,gender,add_notes)
    else:
        return -1

@app.route('/home_test', methods=['GET','POST'])
def home_test():
    if request.method == 'POST':
        print("home_test post method called!")
        print(requests.form)
    return render_template('home_test.html')

@app.route('/home', methods=['GET','POST'])
def home():
    dynamo_client = boto3.client('dynamodb')
    out = []
    # Get appointment details
    app_details = dynamo_client.scan(TableName='appointment_times')
    res_app = app_details['Items']
    pageNumber = 1
    pageLimit = 4
    # skip = (pageNumber - 1) * pageLimit
    print(len(res_app))
    for i in range(len(res_app)):
        title= res_app[i]['apptTitle']['S']
        s_day= res_app[i]['startDay']['S']
        e_day= res_app[i]['endDay']['S']
        c_name = res_app[i]['className']['S']
        p_id= res_app[i]['patientID']['S']
        response = filter_patient_details(p_id)
        if response != -1:
            #print(type(response),response)
            out.append({
                "title":title,
                "s_day":s_day,
                "e_day":e_day,
                "c_name":c_name,
                "fname":response[0],
                "lname":response[1],
                "e_id":response[2],
                "gen":response[3],
                "notes":response[4]         
                })
    result = out

    print("result len: ", len(result))
    # apptTimes = result.query.paginate(page=len(res_app), per_page=3)
    # print(int(math.ceil(len(result)/pageLimit)))
    return render_template('home_test.html',value=result,length0=len(result),totalPages=int(math.ceil(len(result)/pageLimit)))

@app.route('/fullcalendar', methods=['GET', 'POST'])
def fullcalendar():
    appointment_times = dynamodb.Table('appointment_times')
    data = json.dumps(appointment_times.scan()['Items'])
    # data = json.dumps({'username': 'Pang', 'site': 'stackoverflow.com'})
    # print(data)
    # data = "Linda Nguyen"

    # if request.method == 'GET': 
    #     appointment_times = dynamodb.Table('appointment_times')
    #     print("----appointment_times----")
    #     print(appointment_times.scan()['Items'][0])
    #     data = appointment_times.scan()['Items'][0]
    #     x = requests.post("http://127.0.0.1:5000/fullcalendar", data = data)
    #     print("status code: ", x.status_code)

    #     if x.status_code == 200: 
    #         print("Successfully scanned and posted appointment times!")
    #     else: 
    #         print("Failed to scan and post appointment times!")
    if request.method == 'POST':
        apptDetails = request.form.to_dict()
        print("json data ", apptDetails)
        apptTitle = apptDetails['title']
        patientName = apptDetails['patient_name']
        startDay = apptDetails['start']
        endDay = apptDetails['end']
        className = apptDetails['className']
        spot_id = uuid.uuid4() # Unique identifier for spot
        # scan patient details
        patient_details = dynamodb.Table('patient_details')
        row = patient_details.scan(FilterExpression=Key('first_name').eq(patientName))
        patient_uuid = row['Items'][0]['uuid']
        # insert appointment data into table
        appointment_table = dynamodb.Table('appointment_times')
        print("Details: ", spot_id, apptTitle, startDay, endDay, className, patient_uuid)
        appointment_table.put_item(
        Item={  'uuid': str(spot_id),
                'apptTitle': apptTitle,
                'startDay': startDay,
                'endDay': endDay,
                'className': className,
                'patientID': patient_uuid
            }
        )

    return render_template('fullcalendar.html', data = data)

@app.route('/register_patient', methods=['GET','POST'])
def register_patient():
    patientDetails = "none"
    appointment_times = dynamodb.Table('appointment_times')
    data = appointment_times.scan()['Items'][0]
    print(appointment_times.scan()['Items'])
    if request.method == "POST": 
        # retrieve data from form
        patientDetails = request.form
        # Unique identifier for spot
        spot_id = uuid.uuid4() 
        # use to store in appt db
        patient_uuid = spot_id 
        first_name = patientDetails['first_name']
        last_name = patientDetails['last_name']
        email = patientDetails['email']
        age_range = patientDetails['age_range']
        gender = patientDetails['gender']
        admission_type = patientDetails['admission_type']
        illness_severity = patientDetails['illness_severity']
        department = patientDetails['department']
        no_of_visits = patientDetails['no_of_visitors']
        admission_deposit = patientDetails['admission_deposit']
        additional_info = patientDetails['additional_info']

        # append values into array via its index
        allFormDetails[6] = department
        allFormDetails[10] = admission_type
        allFormDetails[11] = illness_severity
        allFormDetails[12] = no_of_visits
        allFormDetails[13] = age_range
        allFormDetails[14] = admission_deposit
        print("------------All Patient details-----------------")
        print(allFormDetails)

        table = dynamodb.Table('patient_details')
        print("Details",first_name,last_name,email,age_range,admission_deposit,illness_severity,department,no_of_visits)
        table.put_item(
        Item={  'uuid': str(spot_id),
                'email': email,
                'first_name': first_name,
                'last_name': last_name,
                'age':age_range,
                'gender':gender,
                'admission_type':admission_type,
                'illness_severity':illness_severity,
                'department':department,
                'no_of_visits':no_of_visits,
                'admission_deposit':admission_deposit,
                'additional_info':additional_info
            }
        )
        return redirect('/estimate_stay')
    return render_template('register_patient.html', data = data)

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
        #print("hospital details: ", request.form)

        allFormDetails[0] = str(caseID)
        allFormDetails[1] = h_code
        allFormDetails[2] = ht_code
        allFormDetails[3] = hc_code
        allFormDetails[4] = hr_code
        allFormDetails[5] = room_availability
        allFormDetails[7] = ward_type
        allFormDetails[8] = ward_facility
        allFormDetails[9] = bed_grade
        print("------------All details-----------------")
        print(allFormDetails)
        spot_id = uuid.uuid4() #Unique identifier for spot

        #print(h_code,ht_code)
        table = dynamodb.Table('hosp_details')
        table.put_item(
        Item={  'uuid': str(spot_id),
                'h_code': h_code,
                'ht_code': ht_code,
                'hc_code': hc_code,
                'hr_code':ht_code,
                'room_availability':room_availability,
                'ward_type':ward_type,
                'ward_facility':ward_facility,
                'bed_grade':bed_grade
            }
        )
        # calculate LoS
        los = makecalc()
        return render_template('fullcalendar.html', los = los[1], displayLos = True);
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
    modelInput = []
    modelInput.append(allFormDetails)
    print("model input: ", modelInput)
    prediction = np.array2string(model.predict(modelInput))
    print("prediction for random data: ", prediction)
    return prediction

if __name__ == "__main__":
    app.run(debug=True)
   

   # flask with ML
   #https://www.youtube.com/watch?v=UbCWoMf80PY&feature=emb_logo
