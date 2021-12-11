from flask import render_template, flash, redirect, url_for, request, abort
from flask_login import current_user, login_user, logout_user, login_required

from app import app, login, db
from app.models import User


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


@app.route("/", methods=["GET", "POST"])
def index():
    return render_template('index.html')


@app.route("/login-request", methods=["GET", "POST"])
def login():
    """
    handle ajax request;
    geting form data from login form,
    check if email exist and password is correct
    the log user in.
    """
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        user = User.query.filter_by(email=email).first()
        if user and not user.check_password(password):
            abort(404)
        login_user(user)
    return redirect(url_for("index"))


@app.route("/signup", methods=["GET", "POST"])
def signup():
    """
    handle ajax request;
    geting form data from signup form,
    add data to database.
    """
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        phone = request.form.get("phone")
        password = request.form.get("password1")
        user = User(name=name, email=email, phone=phone)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for("login"))
    return render_template("sign_up.html", title="Sign up")



@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for("index"))


@app.route("/user/account", methods=["GET", "POST"])
@login_required
def user_account():
    return render_template('user_account.html')
