# Patient_Connect 
**Course:** Cmpe 280
PatientConnect is a healthcare management app that can be used to book hospital bedrooms for patients that need to be admitted. Our app will deploy a model that will predict a patient’s length of stay (LoS) based on their age and condition severity. By applying this machine learning model, hospital staff can better allocate resources and optimize procedures.

## Install Requirements
```
pip install -r requirements.txt
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
[AV: Healthcare Analytics II](https://www.kaggle.com/nehaprabhavalkar/av-healthcare-analytics-ii)
There are two files provided: the training and test data set. The datasets has information regarding the hospital region, department, patient severity, number of rooms, etc. Based on this info, we can use the training data set to create a model that will predict the LoS based on the test data set.