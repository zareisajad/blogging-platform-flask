from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms.fields.simple import TextAreaField
from wtforms.validators import DataRequired
from wtforms import StringField


class AddPostForm(FlaskForm):
    featuring_image = FileField(
        render_kw={'accept': 'image/*'},
        validators=[FileAllowed(['jpg', 'png', 'jpeg'])]
    )
    title = StringField(
        render_kw={'placeholder': 'Example(How to create a flask app!)'},
        validators=[DataRequired()]
    )
    