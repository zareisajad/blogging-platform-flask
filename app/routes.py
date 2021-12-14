from flask import render_template, flash, redirect, url_for, request, abort
from flask_login import current_user, login_user, logout_user, login_required

from app import app, login, db
from app.models import User, Category
from app.forms import AddPostForm


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


@app.route("/", methods=["GET", "POST"])
def index():
    return render_template('index.html')


@app.route("/login-request", methods=["GET", "POST"])
def login():
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
    if request.method == "POST":
        fname = request.form.get("fname")
        lname = request.form.get("lname")
        username = request.form.get("username")
        email = request.form.get("email")
        phone = request.form.get("phone")
        password1 = request.form.get("password1")
        password2 = request.form.get("password1")
        check_username = User.query.filter_by(username=username).first()
        check_email = User.query.filter_by(email=email).first()
        if check_email:
            flash("""
                there is another user with this email! is that you? if yes.
                plese login to your account""",
                category='danger'
            )
            return redirect(url_for('signup'))
        if check_username:
            flash('this username is not avaiable!', category='danger')
            return redirect(url_for('signup'))
        if password1 != password2:
            flash('both password fields should be match!', category='danger')
            return redirect(url_for('signup'))
        user = User(
            username=username, email=email,
            fname=fname, lname=lname, phone=phone
        )
        user.set_password(password1)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template("sign_up.html", title="Sign up")


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for("index"))


@app.route("/user/account", methods=["GET", "POST"])
@login_required
def user_account():
    return render_template('user_account.html')


@app.route("/add/post", methods=["GET", "POST"])
@login_required
def add_post():
    form = AddPostForm()
    return render_template('add_post.html', form=form, title='Add Post')


@app.route("/add/category", methods=["GET", "POST"])
@login_required
def add_category():
    if request.method == 'POST':
        title = request.form.get('category')
        if not Category.query.filter_by(title=title).first():
            category = Category(title=title)
            db.session.add(category)
            db.session.commit()
            return redirect(url_for("add_post"))
    return redirect(url_for("add_post"))

