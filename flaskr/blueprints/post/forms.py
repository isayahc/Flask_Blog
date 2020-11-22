from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField
from wtforms.fields.simple import SubmitField
from wtforms.validators import DataRequired

from flaskr import pagedown

class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()])
    submit = SubmitField('Post')

