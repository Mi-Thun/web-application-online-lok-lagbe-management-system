from flask import *
from flask import Flask, render_template, redirect, request, session
from flask_session import Session
import pymongo
from bson.objectid import ObjectId
from flask_mail import *

app = Flask(__name__)

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


@app.route("/")
def index():
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
        list.append(data)
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


# @app.route('/blog/', methods=["GET", "POST"])
# def blog():
#     edit = False
#     pre_id1 = ''
#     if request.args.get('id') is not None:
#         if request.args.get('typ') == 'dlt':
#             idf = request.args.get('id')
#             Blog_Info.delete_one({'_id': ObjectId(idf)})
#         if request.args.get('typ') == 'edit':
#             edit = True
#             idf = request.args.get('id')
#             infoB = Blog_Info.find_one({'_id': ObjectId(idf)})
#             pre_tittle = infoB['tittle']
#             pre_content = infoB['content']
#             pre_id = infoB['_id']
#             pre_id1 = pre_id
#             pre_photo = infoB['image']
#     else:
#         f = "Don't have any id"
#     list = []
#     havePost = False
#     isPost = False
#     for data in Blog_Info.find():
#         list.append(data)
#         havePost = True
#     result = ''
#     isPost = False
#     if request.method == "POST":
#         isPost = True
#         email = session['email']
#         tittle = request.form['tittle']
#         content = request.form['content']
#         image = request.form['image']
#         print(request.form['ide'])
#         print(pre_id1)
#         if request.form['ide'] == pre_id1:
#             try:
#                 Blog_Info.delete_one({'_id': ObjectId(pre_id1)})
#                 Blog_Info.insert_one({'tittle': tittle, 'content': content, 'image': image, 'email': email})
#                 result = "Update Successfully"
#                 print('yes')
#                 return render_template("blog.html", **locals())
#             except:
#                 f = 'fdvfd'
#         else:
#             print('no')
#             Blog_Info.insert_one({'tittle': tittle, 'content': content, 'image': image, 'email': email})
#             result = "Insert Successfully"
#             return render_template("blog.html", **locals())
#     return render_template("blog.html", **locals())
#

@app.route('/logout/')
def logout():
    session.clear()
    return render_template("index.html", **locals())


@app.route('/about/')
def about():
    return render_template("about.html")


@app.route('/service/<string:n>/', methods=["GET", "POST"])
def service(n):
    n = str(n)
    list = []
    listS = []
    isPost = False
    if request.method == 'POST':
        isPost = True
        f = request.form
        s = f['search']
        # s = s.split(" ")
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
        address = form_data['address']
        Work_Description = form_data["Work_Description"]
        name = form_data['name']
        phonenumber = form_data['phonenumber']
        email = form_data['email']
        dict = {'start_date': start_date, 'end_date': end_date, 'Start_Time': Start_Time,
                'end_time': end_time, 'Worker_uid': Worker_uid, 'address': address,
                'Work_Description': Work_Description,
                'name': name, 'phonenumber': phonenumber, 'email': email}
        deal_info.insert_one(dict)
        return render_template("index.html", **locals())
    return render_template("client.html", **locals())


if __name__ == '__main__':
    app.run(debug=True)
