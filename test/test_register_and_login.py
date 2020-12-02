import unittest
from selenium import webdriver
import requests

# change this path executable to your own to execute this script!!
driver = webdriver.Chrome("/Users/lindanguyen/Desktop/Patient_Connect/chromedriver")
register_url = "http://127.0.0.1:5000/register"
login_url = "http://127.0.0.1:5000/login"

# registration fields
first_name = "John"
last_name = "Doe"
email = "john_doe@gmail.com"
password = "12"


class TestRegisterAndLogin(unittest.TestCase): 
    def test_register(self):
        # automate register
        driver.get(register_url)
        driver.find_element_by_name('f_name').send_keys(first_name)
        driver.find_element_by_name('l_name').send_keys(last_name)
        driver.find_element_by_name('email').send_keys(email)
        driver.find_element_by_name('password').send_keys(password)
        driver.find_element_by_name('license_checkbox').click()
        driver.find_element_by_name('register_button').click()
        # check status code 200
        code = requests.get(register_url)
        print("register status code: ", code.status_code)
        self.assertEqual(code.status_code, 200)

    def test_login(self):
        # automate login
        driver.get(login_url)
        driver.find_element_by_name('email').send_keys(email)
        driver.find_element_by_name('password').send_keys(password)
        driver.find_element_by_name('login_button').click()
        # check status code 200
        code = requests.get(login_url)
        print("login status code: ", code.status_code)
        self.assertEqual(code.status_code, 200)


if __name__ == '__main__':
    unittest.main()