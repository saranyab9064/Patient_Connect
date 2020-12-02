# Patient_Connect HealthCare Application

**Course:** CMPE 280 Web UI

PatientConnect is a healthcare management app that can be used to book hospital bedrooms for patients that need to be admitted. Our app will deploy a model that will predict a patient’s length of stay (LoS) based on their age and condition severity. By applying this machine learning model, hospital staff can better allocate resources and optimize procedures.

## Install Requirements
```
pip install -r requirements.txt
```
## AWS Dynamodb
```
Generate secret and access aws keys
Configure the keys using cli command "aws configure" on local machine
Created three tables
--------------------
1. user_auth [ Stores user information(doctor's info) and validates it ]
2. patient_details [ Stores patient information ]
3. hosp_details [ Stores hospital details ] 
```
## Run Application
In your terminal, run the following:
```
# mac os
export FLASK_APP=main.py

# windows
set FLASK_APP=main.py

# run flask server
flask run
```

## Kaggle Dataset
[AV: Healthcare Analytics II](https://www.kaggle.com/nehaprabhavalkar/av-healthcare-analytics-ii)\
There are two files provided: the training and test data set. The datasets has information regarding the hospital region, department, patient severity, number of rooms, etc. Based on this info, we can use the training data set to create a model that will predict the LoS based on the test data set.

## Selenium 
You need to download [chrome driver](https://sites.google.com/a/chromium.org/chromedriver/downloads) in order to run the automation scripts. Once downloaded, move the executable to the project's root directory. 

We used Selenium to automate the steps on the webpage and performed unit test to make sure each step was successful. 

## Unit Tests
Python interpreter will automatically detect the unit cases as long as files' names start with "test_xxx.py". Most of the unit tests will check for a status code 200 after an action has been performed on the webpage. 

```
cd test
python3 -m unittest
```

## Bugs
If you get the following error: 
```
We have compiled some common reasons and troubleshooting tips at:

    https://numpy.org/devdocs/user/troubleshooting-importerror.html

Please note and check the following:

  * The Python version is: Python3.7 from "/Users/lindanguyen/Desktop/Patient_Connect/venv2/bin/python3"
  * The NumPy version is: "1.19.4"

and make sure that they are the versions you expect.
Please carefully study the documentation linked above for further help.

Original error was: No module named 'numpy.core._multiarray_umath'
```

Try reinstalling numpy. 
```
pip install --upgrade --force-reinstall numpy
```

## Error Handling
```
ValueError: could not convert string to float:
```
Make sure to fill out the required fields. 
