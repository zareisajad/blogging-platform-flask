import os
import bleach

from flask import render_template, flash, redirect, url_for, request, abort
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.utils import secure_filename

from app import app, login, db
from app.models import User, Category, Post, Profile, Comment
from app.forms import AddPostForm, ProfileForm, SignupForm, CommentForm


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
    return redirect(url_for("setting"))


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
        img_name[0] = current_user.username + str(current_user.id) + '.'
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
                about=form.about.data,
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
            return redirect(url_for('profile', username=current_user.username))
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
    return render_template('profile.html', user=user)


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
                styles=app.config['ALLOWED_STYLES']
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
            return redirect(url_for('post_detail', title=post.title))
    return render_template('add_post.html', form=form, title='Add Post')


@app.route("/posts/delete/<id>", methods=["GET", "POST"])
@login_required
def delete_post(id):
    post = Post.query.filter_by(id=id).first_or_404()
    post_image = 'app/static' + post.image
    if os.path.isfile(post_image):
        os.remove(post_image)
    db.session.delete(post)
    db.session.commit()
    flash('post has been deleted!', category='info')
    return redirect(url_for('profile', username=current_user.username))


@app.route("/posts/<title>", methods=["GET", "POST"])
@login_required
def post_detail(title):
    form = CommentForm()
    post = Post.query.filter_by(title=title).first()
    tags = post.tags.split(',')
    comments = Comment.query.all()
    if form.validate_on_submit():
        comment = Comment(
            comment=form.comment.data,
            username=form.username.data,
            post_id=post.id
        )
        db.session.add(comment)
        db.session.commit()
        flash('Your comment has been published!', category='success')
        return redirect(url_for('post_detail', title=post.title))
    if request.method == 'GET':
        form.username.data = current_user.username
    return render_template(
        'post_detail.html', post=post, tags=tags, comments=comments, form=form
    )


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


@app.route("/filter/category/<category>", methods=["GET", "POST"])
@login_required
def filter_by_category(category):
    c = Category.query.filter_by(title=category).first()
    posts = Post.query.filter_by(category_id=c.id).all()
    return render_template('explore.html', posts=posts)


@app.route("/filter/tag/<tag>", methods=["GET", "POST"])
@login_required
def filter_by_tags(tag):
    posts = Post.query.filter(Post.tags.contains(tag)).all()
    return render_template('explore.html', posts=posts)
