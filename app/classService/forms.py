from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, TextAreaField, FloatField, SubmitField, BooleanField
from flask_wtf.file import FileRequired, FileAllowed, FileField
from wtforms.validators import DataRequired
from . import quiz_archive, video_file, lecture_file

class CourseForm(FlaskForm):
    id          = StringField(u'Course Id', validators=[])
    name        = StringField(u'Course Name', validators=[DataRequired(message="You must provide a course name.")])
    author      = StringField(u'Authors', validators=[DataRequired("You must provide the author(s) name.")], default="Various")
    expires     = IntegerField(u'Expiry in weeks', description='Set number of weeks before course expires once started. Leave black for 1 year')
    ppercent    = FloatField(u'Percent Score Required for Certification', default=70.00)
    description = TextAreaField(u'Course Description', default='Write a few words to describe this course.')
    ready       = BooleanField(u'Course Available?')
    submit      = SubmitField(u'Create/Update Course')

class SegmentForm(FlaskForm):
    id          = StringField(u'Segment Id', validators=[])
    name        = StringField(u'Segment Name', validators=[DataRequired("You must provide a segment name")])
    author      = StringField(u'Authors', default="Various")
    required    = BooleanField(u'Segment Required Before Continuing?')
    submit      = SubmitField(u'Create/Update Segment')

class QuizForm(FlaskForm):
    id          = StringField(u'Quiz Id', validators=[])
    name        = StringField(u'Name of Quiz', validators=[DataRequired("You must provide a quiz name")])
    maxscore    = FloatField(u'Total Points', description='Maximum Points this Quiz is worth. Leave blank for QuizMaker Points')
    quiz        = FileField(u'Upload Quiz Archive', validators=[FileAllowed(quiz_archive, 'Quiz Archives Online!')])
    estimated   = IntegerField(u'Estimated Time in Minutes', description='Estimated time in minutes. Leave blank for no estimate.')
    required    = BooleanField(u'Is the quiz required to process in segment?')
    submit      = SubmitField(u'Add/Modify Quiz')

class VideoForm(FlaskForm):
    id          = StringField(u'Video Id', validators=[])
    name        = StringField(u'Name of Video', validators=[DataRequired("You must provide a video title")])
    video       = FileField(u'Upload Video', validators=[FileAllowed(video_file, 'Allowed format: mp4, webm')])
    required    = BooleanField(u'Is this video required to process in segment?')
    submit      = SubmitField(u'Add/Modify Video')

class LectureForm(FlaskForm):
    id          = StringField(u'Lecture Id', validators=[])
    name        = StringField(u'Name for these Slides', validators=[DataRequired("You must provide a lecture title")])
    lecture     = FileField(u'Upload Lecture File', validators=[FileAllowed(lecture_file, 'Allowed format: ppt, pdf, pptx')])
    required    = BooleanField(u'Is the lecture required to process in segment?')
    submit      = SubmitField(u'Add/Modify Lecture')

