from random import randint

from flask import Flask, render_template, request, session
import pymongo
from bson.objectid import ObjectId
from flask_mail import *
import time

app = Flask(__name__)

app = Flask(__name__)
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'mohsenulkabirmi8486@gmail.com'
app.config['MAIL_PASSWORD'] = ''
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True

app.config.from_object(__name__)
mail = Mail(app)

app.secret_key = 'super secret key'

myDB = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myDB["Lok_Lagbe"]
user_info = mydb["user_info"]
worker_info = mydb["worker_info"]
deal_info = mydb["deal_info"]
feedback = mydb["feedback"]
contact_info = mydb["contact_info"]
client_info = mydb["client_info"]
Blog_Info = mydb["Blog_Info"]
pass_recover_info = mydb["pass_recover_info"]


@app.route("/")
def index():
    try:
        NumberOfworker = len(list(worker_info.find()))
        NumberOfClient = len(list(client_info.find()))
        NumberOfdeal = len(list(deal_info.find()))
        if session["logged_in"]:
            se = []
            user = worker_info.find_one({'email': session["email"]})
            id = str(user['_id'])
            for sen in deal_info.find({'Worker_uid': id, 'seen': 'no'}):
                se.append(dict(sen))
            lengt = len(se)
            if len(se) > 0:
                haveNoti = True
            else:
                haveNoti = False
    except:
        c =''
    if request.args.get('id') is not None:
        idf = request.args.get('id')
        a = deal_info.find_one({'_id': ObjectId(idf)})
        print(a)
        del a["_id"]
        a['seen'] = 'yes'
        print(a)
        deal_info.delete_one({'_id': ObjectId(idf)})
        deal_info.insert_one(dict(a))
        se = []
        user = worker_info.find_one({'email': session["email"]})
        id = str(user['_id'])
        for sen in deal_info.find({'Worker_uid': id, 'seen': 'no'}):
            se.append(dict(sen))
        lengt = len(se)
        if len(se) > 0:
            haveNoti = True
        else:
            haveNoti = False

    return render_template('index.html', **locals())


@app.route("/login/", methods=["GET", "POST"])
def login():
    error = ""
    try:
        if session["logged_in"]:
            return render_template("index.html ", **locals())
    except:
        if request.method == "POST":
            form_data = request.form
            useremail = form_data["your_email"]
            password = form_data["your_pass"]
            result = user_info.find_one({"email": useremail, "pass": password})
            if result is None:
                error = "Enter valid information"
            else:
                error = "Login Successful."
            if error == "Login Successful.":
                session["logged_in"] = True
                session["email"] = useremail
                session["name"] = result['name']
                return render_template("index.html ", **locals())
    return render_template("login.html", **locals())


@app.route('/signup/', methods=["GET", "POST"])
def signup():
    isPost = False
    message = ''
    agree = 'no'
    if request.method == "POST":
        isPost = True
        form_data = request.form
        name = form_data["name"]
        email = form_data["email"]
        pass1 = form_data["pass"]
        pass2 = form_data["re_pass"]
        try:
            worker_type = str(form_data['agree-term1'])
        except:
            worker_type = 'no'
        try:
            agree = form_data['agree-term']
        except:
            agree = 'no'
        if agree == 'no':
            message = 'please agree our terms and condition'
            print(message)
        else:
            check_user = user_info.find_one({"email": email})
            if pass1 == pass2:
                if check_user is not None:
                    message = 'This email address already register'
                    print(message)
                else:
                    user_info.insert_one({'name': name, 'email': email, 'pass': pass1, 'workertype': worker_type})
                    message = "Successfully complete registration"
                    print(message)
            else:
                message = 'Enter same password'
                print(message)
            if message == "Successfully complete registration":
                return render_template("index.html ", **locals())
    return render_template("signup.html", **locals())


@app.route('/userprofile/', methods=["GET", "POST"])
def userprofile():
    isPost = False
    visibility1 = 'hidden'
    result = user_info.find_one({"email": session["email"]})
    if request.method == "POST":
        isPost = True

    if result['workertype'] == 'on':
        info = worker_info.find_one({"email": session["email"]})
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
            user_info.delete_one({"email": session["email"]})
            user_info.insert_one({'name': name, 'email': email, 'pass': pass1, 'workertype': result['workertype']})
            dict = {'name': name, 'phone': phone, 'age': age, 'sex': sex,
                    'email': email, 'nid': nid, 'address': address, 'postcode': postcode,
                    'area': area, 'city': city, 'parea': parea, 'experience': experience,
                    'additional': additional, 'sat': sat, 'sun': sun, 'mon': mon,
                    'tue': tue, 'wed': wed, 'thr': thr, 'ffri': ffri, 'type': type,
                    'charge': charge, 'pass1': pass1}
            worker_info.insert_one(dict)
            session["email"] = email
            session["name"] = name
            return render_template("index.html", **locals())

    if result['workertype'] == 'no':
        info = client_info.find_one({"email": session["email"]})
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
            pass1 = result['pass']
            user_info.delete_one({"email": session["email"]})
            user_info.insert_one({'name': name, 'email': email, 'pass': pass1, 'workertype': result['workertype']})
            dict = {'name': name, 'phone': phone, 'age': age, 'sex': sex,
                    'email': email, 'nid': nid, 'address': address, 'postcode': postcode,
                    'area': area, 'city': city}
            client_info.insert_one(dict)
            session["email"] = email
            session["name"] = name
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


@app.route('/organization/', methods=["GET", "POST"])
def organization():
    return render_template("organization.html")


@app.route('/blog/', methods=["GET", "POST"])
def blog():
    edit = False
    if request.args.get('id') is not None:
        if request.args.get('typ') == 'dlt':
            idf = request.args.get('id')
            Blog_Info.delete_one({'_id': ObjectId(idf)})
        if request.args.get('typ') == 'edit':
            edit = True
            idf = request.args.get('id')
            infoB = Blog_Info.find_one({'_id': ObjectId(idf)})
            pre_tittle = infoB['tittle']
            pre_content = infoB['content']
            pre_id = infoB['_id']
            pre_photo = infoB['image']
    else:
        f = "Don't have any id"
    list = []
    havePost = False
    isPost = False
    for data in Blog_Info.find():
        a = user_info.find_one({'email': data['email']})
        data['name'] = a['name']
        list.append(data)
        print(data)
        havePost = True
    print(list)
    result = ''
    isPost = False
    if request.method == "POST":
        isPost = True
        email = session['email']
        tittle = request.form['tittle']
        content = request.form['content']
        image = request.form['image']
        try:
            Blog_Info.delete_one({'_id': ObjectId(request.form['ide'])})
        except:
            print('done')
        Blog_Info.insert_one({'tittle': tittle, 'content': content, 'image': image, 'email': email})
        result = "Insert Successfully"
        print({'tittle': tittle, 'content': content, 'image': image})
        return render_template("blog.html", **locals())
    return render_template("blog.html", **locals())


@app.route('/logout/')
def logout():
    session.clear()
    return render_template("index.html", **locals())


@app.route('/about/')
def about():
    return render_template("about.html")


@app.route('/forgetPassword/', methods=["GET", "POST"])
def forgetPassword():
    if request.method == 'POST':
        email = request.form['email']
        if email == '':
            message = 'Enter email address'
            return render_template("forgetPassword.html", **locals())
        else:
            user = user_info.find_one({'email': email})
            if user is not None:
                otp = randint(0000, 9999)
                message = 'Check your mailbox. Link will valid only for 5 minutes.'
                pass_recover_info.insert_one({'email': email, 'otp': otp})
                msg = Message('Password recover link..', sender='mohsenulkabirmi8486@gmail.com',
                              recipients=[email])
                msg.body = "http://127.0.0.1:5000/changePassword/" + str(user['_id']) + str(otp)
                mail.send(msg)
                time.sleep(300)
                pass_recover_info.delete_one({'email': email, 'otp': otp})
    return render_template("forgetPassword.html", **locals())


@app.route('/changePassword/<string:n>', methods=["GET", "POST"])
def changePassword(n):
    a = pass_recover_info.find_one({'otp': int(n[24:])})
    print(a)
    find = user_info.find_one({'_id': ObjectId(n[:24])})
    if request.method == 'POST':
        pass1 = request.form['pass1']
        pass2 = request.form['pass2']
        if a:
            if pass1 == pass2:
                find['pass'] = pass1
                user_info.delete_one({'email': find['email']})
                user_info.insert_one(dict(find))
                pass_recover_info.delete_one({'email': find['email']})
                return render_template("login.html", **locals())
    return render_template("changePassword.html", **locals())


@app.route('/service/<string:n>/', methods=["GET", "POST"])
def service(n):
    n = str(n)
    if n == 'helping_hand':
        typ = 'Helping Hand '
    elif n == 'plamber':
        typ = 'Plamber'
    elif n == 'electrician':
        typ = 'Electrician'
    elif n == 'chef':
        typ = 'Chef'
    elif n == 'driver':
        typ = 'Driver'
    elif n == 'baby_setter':
        typ = 'Baby Setter'

    list = []
    listS = []
    isPost = False
    if request.method == 'POST':
        isPost = True
        f = request.form
        s = f['search']
        for form_data in mydb.worker_info.find({'type': n, 'area': f['search']}):
            listS.append(form_data)
    for form_data in mydb.worker_info.find({'type': n}):
        list.append(form_data)
    if len(listS) == 0:
        message = 'No data found'
    else:
        message = 'Your search result:'
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
        worker_details = worker_info.find_one(ObjectId(Worker_uid))
        worker_email = worker_details['email']
        address = form_data['address']
        Work_Description = form_data["Work_Description"]
        name = form_data['name']
        phonenumber = form_data['phonenumber']
        email = form_data['email']

        dict = {'start_date': start_date, 'end_date': end_date, 'Start_Time': Start_Time,
                'end_time': end_time, 'Worker_uid': Worker_uid, 'address': address,
                'Work_Description': Work_Description,
                'name': name, 'phonenumber': phonenumber, 'email': email, 'seen': 'no'}
        deal_info.insert_one(dict)
        msg = Message('New offer arrived', sender='mohsenulkabirmi8486@gmail.com', recipients=[worker_email])
        msg.body = "You have a new offer by '"+ name + "'.Work Details, start_date:"+ start_date+ '; end_date:'+ end_date+ '; Start_Time:'+ Start_Time+ '; end_time:'+ end_time+'; address:'+address+'; Work_Description:'+ Work_Description+'; phonenumber:'+phonenumber+'; email:'+email
        mail.send(msg)
        return render_template("index.html", **locals())
    return render_template("client.html", **locals())


if __name__ == '__main__':
    app.run(debug=True)
