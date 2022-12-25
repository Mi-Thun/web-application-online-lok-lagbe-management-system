from flask import *
from flask import Flask, render_template, redirect, request, session
from flask_session import Session
import pymongo

app = Flask(__name__)

myDB = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myDB["Lok_Lagbe"]
user_info = mydb["user_info"]
worker_info = mydb["worker_info"]
deal_info = mydb["deal_info"]
feedback = mydb["feedback"]
contact_info = mydb["contact_info"]


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
        print(form_data)
        name = form_data["name"]
        email = form_data["email"]
        pass1 = form_data["pass"]
        pass2 = form_data["re_pass"]
        agree = form_data['agree-term']
        try:
            worker_type = str(form_data['agree-term1'])
        except:
            worker_type = 'no'
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


@app.route('/contact/', methods=["GET", "POST"])
def contact():
    isPost = False
    if request.method == "POST":
        isPost = True

    if isPost:
        form_data = request.form
        name = form_data["name"]
        email = form_data["email"]
        subject = form_data["subject"]
        message = form_data["message"]

        dict = {'name': name, 'email': email, 'subject': subject, 'message': message}
        contact_info.insert_one(dict)
    return render_template("contact.html")


@app.route('/blog/')
def blog():
    return render_template("blog.html")


@app.route('/about/')
def about():
    return render_template("about.html")


@app.route('/service/<string:n>/')
def service(n):
    n = str(n)
    print(n)
    list = []
    for form_data in mydb.worker_info.find({'type': n}):
        list.append(form_data)
    return render_template("service.html", **locals())


@app.route('/client/', methods=["GET", "POST"])
def client():
    worker = request.args.get('my_var')
    form_data = worker_info.find_one({"email": worker})
    print(form_data)

    isPost = False
    if request.method == "POST":
        isPost = True

    if isPost:
        form_data = request.form
        print(form_data)
        start_date = form_data["start_date"]
        end_date = form_data["end_date"]
        Start_Time = form_data["Start_Time"]
        end_time = form_data["end_time"]
        Worker_uid = form_data['Worker_uid']
        address = form_data['address']
        Work_Description = form_data["Work_Description"]
        name = form_data['name']
        phonenumber = form_data['phonenumber']
        email = form_data['email']
        dict = {'start_date': start_date, 'end_date': end_date, 'Start_Time': Start_Time,
                'end_time': end_time, 'Worker_uid': Worker_uid, 'address': address, 'Work_Description': Work_Description,
                'name': name, 'phonenumber': phonenumber, 'email': email}
        deal_info.insert_one(dict)
        return render_template("index.html", **locals())
    return render_template("client.html", **locals())


if __name__ == '__main__':
    app.run(debug=True)
