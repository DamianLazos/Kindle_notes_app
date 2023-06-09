# ******************************PYTHON LIBRARIES******************************

# ******************************EXTERNAL LIBRARIES****************************
from flask_wtf import FlaskForm
from wtforms import (StringField, 
                    IntegerField, 
                    FileField,
                    SubmitField)
from wtforms.validators import InputRequired, NumberRange
from flask_wtf.file import FileAllowed, FileRequired
# ******************************OWN LIBRARIES*********************************

# ****************************************************************************
class BookForm(FlaskForm):
    name = StringField("name", validators=[InputRequired(message="Please enter a name for this book.")])
    author = StringField("author", validators=[InputRequired(message="Please enter the name of the author.")])
    year = IntegerField("year")
    original_language = StringField("original_language")
    description = StringField("desciption")
    submit = SubmitField()

class BookAddNotes(FlaskForm):
    notesFile = FileField("file", validators=[FileAllowed(["csv"], message="Only .csv files are allowed"), FileRequired(message="Please choose a file.")])
    submit = SubmitField()
    
class BookEditInfo(FlaskForm):
    name = StringField("name")
    author = StringField("author")    
    year = IntegerField("year")
    original_language = StringField("original_language")
    description = StringField("description")
    submit = SubmitField()
    