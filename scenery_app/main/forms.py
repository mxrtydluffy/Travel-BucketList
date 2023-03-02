# Create your forms here.

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, DateField, SelectField, SubmitField, TextAreaField
from wtforms.ext.sqlalchemy.fields import QuerySelectField, QuerySelectMultipleField
# from wtforms_sqlalchemy.fields import QuerySelectField, QuerySelectMultipleField
from wtforms.validators import DataRequired, Length
from scenery_app.models import Landscape, List, Entry

class LocationForm(FlaskForm):
    """
    Form to create a location
    """
    title = StringField('Location Title',
        validators=[DataRequired(), Length(min=3, max=80)])
    visited_date = DateField('Location Visited or When Will Visit:')
    list = QuerySelectField('List',
        query_factory=lambda: List.query, allow_blank=False)
    landscape = SelectField('Landscape', choices=Landscape.choices())
    entries = QuerySelectMultipleField('Entries',
        query_factory=lambda: Entry.query)
    submit = SubmitField('Submit')

class ListForm(FlaskForm):
    """
    Form to create a list to create location.
    """
    name = StringField('List Name',
        validators=[DataRequired(), Length(min=3, max=80)])
    description = TextAreaField('List Description')
    submit = SubmitField('Submit')


class EntryForm(FlaskForm):
    """
    Form to create a entry.
    """
    name = StringField('Entry:',
        validators=[DataRequired(), Length(min=3, max=700)])
    submit = SubmitField('Submit')