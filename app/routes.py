import os
import bleach

from flask import render_template, flash, redirect, url_for, request, abort
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.utils import secure_filename

from app import app, login, db
from app.models import User, Category, Post, Profile
from app.forms import AddPostForm, ProfileForm, SignupForm


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


@app.route("/", methods=["GET", "POST"])
def explore():
    posts = Post.query.all()
    return render_template('explore.html', posts=posts)


@app.route("/login-request", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        user = User.query.filter_by(email=email).first()
        if not user or not user.check_password(password):
            abort(404)
        login_user(user)
    return redirect(url_for("explore"))


@app.route("/signup", methods=["GET", "POST"])
def signup():
    form = SignupForm()
    if request.method == "POST":
        if form.validate_on_submit():
            user = User(username=form.username.data, email=form.email.data)
            user.set_password(form.password.data)
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('login'))
    return render_template("sign_up.html", title="Sign up", form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for("explore"))


def upload_img(img_file):
    """
    get img file, secure its name and save it in static/images,
    then return its url to save in db.
    output: /static/images/sajad1.jpg
    """
    img = img_file
    filename = img.filename
    if filename != '':
        img_name = filename.split('.')
        img_name[0] = current_user.profile.fname + str(current_user.id) + '.'
        name = ''.join(img_name)
        filename = secure_filename(name)
        img.save(os.path.join(app.config["UPLOAD_PATH"], filename))
    img_url = os.path.join("/images", filename)
    return img_url


@app.route("/user/setting", methods=["GET", "POST"])
@login_required
def setting():
    form = ProfileForm()
    if form.validate_on_submit():
        if not current_user.profile:        
            profile = Profile(
                avatar=upload_img(form.avatar.data),
                fname=form.fname.data,
                lname=form.lname.data,
                user_id=current_user.id
            )
            db.session.add(profile)
            db.session.commit()
            flash('Profil has been updated!', category='success')
            return redirect(url_for('setting'))
        else:
            # updating profile information
            p = current_user.profile
            p.fname=form.fname.data
            p.lname=form.lname.data
            p.about=form.about.data
            if form.avatar.data:
                p.avatar = upload_img(form.avatar.data)
            db.session.commit()
            flash('Profil has been updated!', category='success')
            return redirect(url_for('setting'))
    else:
        if current_user.profile:
            form.fname.data = current_user.profile.fname
            form.lname.data = current_user.profile.lname
            form.about.data = current_user.profile.about
    return render_template('setting.html', form=form)


@app.route("/user/<username>", methods=["GET", "POST"])
@login_required
def profile(username):
    user = User.query.filter_by(username=username).first()
    return render_template('profile.html')


@app.route("/add/post", methods=["GET", "POST"])
@login_required
def add_post():
    form = AddPostForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            uploaded_file = form.featuring_image.data
            filename = secure_filename(uploaded_file.filename)
            uploaded_file.save(
                os.path.join(app.config["UPLOAD_PATH"], filename)
            )
            url = os.path.join("/images", filename)
            content = bleach.clean(
                request.form.get('editordata'),
                tags=app.config["ALLOWED_TAGS"],
                attributes=app.config["ALLOWED_ATTRIBUTES"],
            )
            category = Category.query.filter_by(
                title=str(form.category.data)
            ).first()
            post = Post(
                image=url,
                title=form.title.data,
                category_id=category.id,
                tags=form.tags.data,
                content=content,
                user_id=current_user.id
            )
            db.session.add(post)
            db.session.commit()
            return redirect(url_for('add_post'))
    return render_template('add_post.html', form=form, title='Add Post')


@app.route("/posts/<title>", methods=["GET", "POST"])
@login_required
def post_detail(title):
    post = Post.query.filter_by(title=title).first()
    return render_template('post_detail.html', post=post)


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


# pass category to base.html
@app.context_processor
def pass_category():
    category = Category.query.filter().all()
    return dict(category=category)


@app.route("/filter/category/<id>", methods=["GET", "POST"])
@login_required
def filter_by_category(id):
    posts = Post.query.filter_by(category_id=id).all()
    return render_template('explore.html', posts=posts)
