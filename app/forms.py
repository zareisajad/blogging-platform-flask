from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.fields.simple import TextAreaField
from wtforms.validators import DataRequired, Email, ValidationError, Length, EqualTo
from wtforms import StringField, PasswordField

from app.models import Category, User


def enabled_categories():
    return Category.query.all()
    

class SignupForm(FlaskForm):
    email = StringField(
        render_kw={'placeholder': 'Email'},
        validators=[DataRequired(), Email(check_deliverability=True)]
    )
    username = StringField(
        render_kw={'placeholder': 'username'},
        validators=[DataRequired()]
    )
    password = PasswordField(
        render_kw={'placeholder': 'password'},
        validators=[DataRequired(),
        Length(min=6,message='password is too short!'),
        EqualTo('confirm_password', message='Passwords must match')]
    )
    confirm_password = PasswordField(
        render_kw={'placeholder': 'repeat password'},
        validators=[DataRequired()]
    )

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('the email is taken!')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('the username is taken!')



class AddPostForm(FlaskForm):
    featuring_image = FileField(
        render_kw={'accept': 'image/*'},
        validators=[DataRequired(), FileAllowed(['jpg', 'png', 'jpeg'])]
    )
    title = StringField(
        render_kw={'placeholder': 'Example(How to create a flask app!)'},
        validators=[DataRequired()]
    )
    category = QuerySelectField(
        query_factory=enabled_categories,
        allow_blank=False,
        validators=[DataRequired()]
    )
    tags = StringField(
        render_kw={'placeholder': 'flask,python,blog'},
        validators=[DataRequired()]
    )


class ProfileForm(FlaskForm):
    avatar = FileField(
        render_kw={'accept': 'image/*'},
        validators=[FileAllowed(['jpg', 'png', 'jpeg'])]
    )
    fname = StringField(
        render_kw={'placeholder': 'name'},
        validators=[DataRequired()]
    )
    lname = StringField(
        render_kw={'placeholder': 'lastname'},
        validators=[DataRequired()]
    )
    about = TextAreaField(
        render_kw={
            'placeholder': 'Tell somthig about yourself...',
            'cols':'30', 'rows':'5'
        },
        validators=[DataRequired()]
    )