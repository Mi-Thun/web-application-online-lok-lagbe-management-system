from flask import *

app = Flask(__name__)


@app.route('/')
def hello_world():
    return render_template("index.html")


@app.route('/login/')
def login():
    return render_template("login.html")


@app.route('/signup/')
def signup():
    return render_template("signup.html")


@app.route('/contact/')
def contact():
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


@app.route('/userprofile/')
def userprofile():
    return render_template("userprofile.html")


if __name__ == '__main__':
    app.run(debug=True)
