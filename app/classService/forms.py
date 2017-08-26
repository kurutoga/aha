from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, TextAreaField, FloatField, SubmitField
from wtforms.validators import DataRequired

class CourseForm(FlaskForm):
    name        = StringField(u'Course Name', validators=[DataRequired(message="You must provide a course name.")])
    author      = StringField(u'Authors', validators=[DataRequired("You must provide the author(s) name.")], default="Various")
    expires     = IntegerFrield(u'Expiry in weeks' description='Set number of weeks before course expires once started. Leave black for 1 year')
    ppercent    = FloatField(u'Percent Score Required for Certification', default=70.00)
    description = TextAreaField(u'Course Description', default='Write a few words to describe this course.')
    ready       = BooleanField(u'Course Available?')
    submit      = SubmitField(u'Create Course')

class SegmentForm(FlaskForm):
    name        = StringField(u'Course Name', validators=[DataRequired("You must provide a segment name")])
    author      = StringField(u'Authors', default="Various")
    estimated   = IntegerField(u'Estimated Time Required in Weeks')
    required    = BooleanField(u'Segment Required Before Continuing?')

class QuizForm(FlaskForm):
    name        = StringField(u'Name of Quiz', validators=[DataRequired("You must provide a quiz name")])
    maxscore    = FloatField(u'Total Points', message='Maximum Points this Quiz is worth. Leave blank for QuizMaker Points')
    quiz        = FileField(u'Upload Quiz Folder', 
