from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.validators import DataRequired
from wtforms import StringField

from app.models import Category


def enabled_categories():
    categories = Category.query.all()
    
    return Category.query.all()
    

class AddPostForm(FlaskForm):
    featuring_image = FileField(
        render_kw={'accept': 'image/*'},
        validators=[FileAllowed(['jpg', 'png', 'jpeg'])]
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


class AddCategoryForm(FlaskForm):
    title = StringField(validators=[DataRequired()])
