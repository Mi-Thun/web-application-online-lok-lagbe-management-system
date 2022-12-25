from flask import *
from flask import Flask, render_template, redirect, request, session
from flask_session import Session
import pymongo

app = Flask(__name__)

myDB = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myDB["Lok_Lagbe"]
user_info = mydb["user_info"]
worker_info = mydb["worker_info"]
feedback = mydb["feedback"]
contact = mydb["contact"]


@app.route("/")
def index():
    return render_template('index.html', **locals())


@app.route("/login/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        form_data = request.form
        useremail = form_data["your_email"]
        password = form_data["your_pass"]
        error = ""
        result = user_info.find_one({"email": useremail, "pass1": password})
        if result is None:
            error = "Enter valid information"
        else:
            error = "Login Successful."
        return render_template("index.html ", **locals())
    return render_template("login.html", **locals())


@app.route('/signup/', methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        form_data = request.form
        name = form_data["name"]
        email = form_data["email"]
        pass1 = form_data["pass"]
        pass2 = form_data["re_pass"]
        agree = form_data['agree-term']
        worker_type = form_data['worker_type']
        user_info.insert_one({'name': name, 'email': email, 'pass': pass1, 'workertype': worker_type})
        message = "Register Successfully"
        return render_template("index.html ", **locals())
    return render_template("signup.html")


@app.route('/userprofile/', methods=["GET", "POST"])
def userprofile():
    isPost = False
    visibility1 = 'hidden'
    result = user_info.find_one({"email": 'mk@gmail.com'})
    info = worker_info.find_one({"email": 'mk@gmail.com'})

    if request.method == "POST":
        isPost = True

    if result['workertype'] == 'on':
        visibility1 = 'visible'
        if isPost:
            form_data = request.form
            print(form_data)
            name = form_data["Name"]
            phone = form_data["Phone Number"]
            age = form_data["Age"]
            sex = form_data["Sex"]
            email = form_data['Email ID']
            nid = form_data['NID']
            address = form_data["Address"]
            postcode = form_data['Postcode']
            area = form_data['Area']
            city = form_data["City"]
            parea = form_data['Preferred area']
            experience = form_data['Experience']
            additional = form_data["Additional Details"]
            sat = form_data['Saturday']
            sun = form_data['Sunday']
            mon = form_data['Monday']
            tue = form_data["Tuesday"]
            wed = form_data['Wednesday']
            thr = form_data['Thursday']
            ffri = form_data["Friday"]
            type = form_data['work_type']
            charge = form_data['Charge per hour']
            pass1 = result['pass']
            user_info.delete_one({"email": 'mk@gmail.com'})
            user_info.insert_one({'name': name, 'email': email, 'pass': pass1, 'workertype': result['worker_type']})
            dict = {'name': name, 'phone': phone, 'age': age, 'sex': sex,
                                  'email': email, 'nid': nid, 'address': address, 'postcode': postcode,
                                  'area': area, 'city': city, 'parea': parea, 'experience': experience,
                                  'additional': additional, 'sat': sat, 'sun': sun, 'mon': mon,
                                  'tue': tue, 'wed': wed, 'thr': thr, 'ffri': ffri, 'type': type,
                                  'charge': charge, 'pass1': pass1}
            print(dict)
            worker_info.insert_one(dict)
            return render_template("index.html", **locals())
    return render_template("userprofile.html", **locals())


@app.route('/contact/')
def contact():
    isPost = False
    visibility1 = 'hidden'
    result = user_info.find_one({"email": 'mk@gmail.com'})
    info = worker_info.find_one({"email": 'mk@gmail.com'})

    if request.method == "POST":
        isPost = True

    if result['workertype'] == 'on':
        visibility1 = 'visible'
        if isPost:
            form_data = request.form
            print(form_data)
            name = form_data["Name"]
            phone = form_data["Phone Number"]
            age = form_data["Age"]
            sex = form_data["Sex"]
            email = form_data['Email ID']
            nid = form_data['NID']
            address = form_data["Address"]
            postcode = form_data['Postcode']
            area = form_data['Area']
            city = form_data["City"]
            parea = form_data['Preferred area']
            experience = form_data['Experience']
            additional = form_data["Additional Details"]
            sat = form_data['Saturday']
            sun = form_data['Sunday']
            mon = form_data['Monday']
            tue = form_data["Tuesday"]
            wed = form_data['Wednesday']
            thr = form_data['Thursday']
            ffri = form_data["Friday"]
            type = form_data['work_type']
            charge = form_data['Charge per hour']
            pass1 = result['pass']
            user_info.delete_one({"email": 'mk@gmail.com'})
            user_info.insert_one({'name': name, 'email': email, 'pass': pass1, 'workertype': result['worker_type']})
            dict = {'name': name, 'phone': phone, 'age': age, 'sex': sex,
                    'email': email, 'nid': nid, 'address': address, 'postcode': postcode,
                    'area': area, 'city': city, 'parea': parea, 'experience': experience,
                    'additional': additional, 'sat': sat, 'sun': sun, 'mon': mon,
                    'tue': tue, 'wed': wed, 'thr': thr, 'ffri': ffri, 'type': type,
                    'charge': charge, 'pass1': pass1}
            print(dict)
            worker_info.insert_one(dict)
            return render_template("index.html", **locals())
    return render_template("contact.html")


@app.route('/blog/')
def blog():
    return render_template("blog.html")


@app.route('/about/')
def about():
    return render_template("about.html")


@app.route('/user/')
def user():
    return render_template("user.html")


@app.route('/service/<string:n>/')
def service(n):
    return render_template("service.html", **locals())


if __name__ == '__main__':
    app.run(debug=True)
