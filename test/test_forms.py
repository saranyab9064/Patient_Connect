import unittest
from selenium import webdriver
from selenium.webdriver.support.ui import Select
import requests
import time

# urls
driver = webdriver.Chrome("/Users/lindanguyen/Desktop/Patient_Connect/chromedriver")
home_url = "http://127.0.0.1:5000/home"
patient_url = "http://127.0.0.1:5000/register_patient"
hospital_url = "http://127.0.0.1:5000/estimate_stay"

# patient details
first_name = "Maxen"
last_name = "Chu"
patient_email = "maxen@gmail.com"
age_group = "0-10"
blood_type = "B+"
no_of_visits = "3"
admission_deposit = "10"
additional_info = "allergic to nuts and eggs"

# hostpital details
h_code = "10"
room_availability =  "14"



class TestPatientAdmission(unittest.TestCase): 

    def test_estimate_los(self): 
        # go to Patient details page
        driver.get(home_url)
        driver.find_element_by_name('patient_admission_nav').click()
        driver.find_element_by_name('estimate_los_drop').click()
        time.sleep(1)
        # check status code 200
        code = requests.get(home_url)
        print("estimate los status code: ", code.status_code)
        self.assertEqual(code.status_code, 200)

    def test_patient_form(self): 
        # fill out patient details
        driver.get(patient_url)
        driver.find_element_by_name('first_name').send_keys(first_name)
        driver.find_element_by_name('last_name').send_keys(last_name)
        driver.find_element_by_name('email').send_keys(patient_email)
        select = Select(driver.find_element_by_name('age_range')).select_by_index(1)
        driver.find_element_by_id('male').click()
        driver.find_element_by_name('blood_type').send_keys(blood_type)
        select = Select(driver.find_element_by_name('admission_type')).select_by_index(1)
        select = Select(driver.find_element_by_name('illness_severity')).select_by_index(2)
        select = Select(driver.find_element_by_name('department')).select_by_index(3)
        driver.find_element_by_name('no_of_visitors').send_keys(no_of_visits)
        driver.find_element_by_name('admission_deposit').send_keys(admission_deposit)
        driver.find_element_by_name('additional_info').send_keys(additional_info)
        time.sleep(1)
        driver.find_element_by_name('submit_button').click()
        # check status code 200
        code = requests.get(home_url)
        print("patient form status code: ", code.status_code)
        self.assertEqual(code.status_code, 200)

    def test_estimate_stay_form(self): 
        # fill out hospital details
        driver.get(hospital_url)
        driver.find_element_by_name('h_code').send_keys(h_code)
        select = Select(driver.find_element_by_name('ht_code')).select_by_index(4)
        select = Select(driver.find_element_by_name('hc_code')).select_by_index(4)
        select = Select(driver.find_element_by_name('hr_code')).select_by_index(2)
        driver.find_element_by_name('room_availability').send_keys(room_availability)
        select = Select(driver.find_element_by_name('ward_type')).select_by_index(3)
        select = Select(driver.find_element_by_name('ward_facility')).select_by_index(2)
        select = Select(driver.find_element_by_name('bed_grade')).select_by_index(3)
        driver.find_element_by_name('estimate_button').click()
        time.sleep(2)  # takes some time for model to calculate los
        # check status code 200
        code = requests.get(hospital_url)
        print("hospital form status code: ", code.status_code)
        self.assertEqual(code.status_code, 200)


if __name__ == '__main__': 
    unittest.main() 

    # test a single case
    # x = TestPatientAdmission()
    # x.test_estimate_stay_form()
