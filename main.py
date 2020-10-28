from flask import Flask,render_template,request
import mysql.connector

app=Flask(__name__)

#conn=mysql.connector.connect(host=)

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/register')
def about():
    return render_template('register.html')

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/calendar')
def calendar():
    return render_template('calendar.html')

@app.route('/book_appointments')
def book_appointments():
    return render_template('book_appointments.html')

@app.route('/settings')
def settings():
    return render_template('settings.html')

@app.route('/login_validation', methods=['POST'])
def login_validation():
    email=request.form.get('email')
    password=request.form.get('password')
    return "The email is {} and the password is {}".format(email,password)


if __name__ == "__main__":
   app.run(debug=True)
   

   # flask with ML
   #https://www.youtube.com/watch?v=UbCWoMf80PY&feature=emb_logo