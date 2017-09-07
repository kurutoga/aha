from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, TextAreaField, FloatField, SubmitField, BooleanField
from flask_wtf.file import FileRequired, FileAllowed, FileField
from wtforms.validators import DataRequired, optional, URL
from wtforms.ext.sqlalchemy.fields import QuerySelectMultipleField
from . import quiz_archive, video_file, lecture_file
from app.classService.controllers import get_elders, get_prerequisites, get_children


def _get_course_form(course_id=None):
    class CourseForm(FlaskForm):
        id          = StringField(u'Course Id', validators=[])
        name        = StringField(u'Course Name', validators=[DataRequired(message="You must provide a course name.")])
        author      = StringField(u'Authors', validators=[DataRequired("You must provide the author(s) name.")], default="Various")
        expires     = IntegerField(u'Expiry (in weeks)', [optional()], description='Set number of weeks before course expires once started. Leave blank for 1 year')
        ppercent    = FloatField(u'Percent Score Required for Certification', default=70.00)
        description = TextAreaField(u'Course Description', default='Write a few words to describe this course.')
        ready       = BooleanField(u'Course Available?')
        prereq      = QuerySelectMultipleField(u'Select Prerequisites for this course', allow_blank=True, query_factory=lambda: get_elders(course_id) if course_id else get_children(None), default=lambda: get_prerequisites(course_id) if course_id else [], get_pk=lambda item: item.id, get_label=lambda item: item.name, description="Leave blank for no prereq. Use 'Shift' and 'Ctrl/Cmd' for multiple selection/deselection")
        videolink   = StringField(u'External Video Link', validators=[URL(), optional()], description='Youtube/Other External Video Playlist Link')
        submit      = SubmitField(u'Create/Update Course')
    return CourseForm

def _get_segment_form(course_id, segment_id=None):
    class SegmentForm(FlaskForm):
        id          = StringField(u'Segment Id', validators=[])
        name        = StringField(u'Segment Name', validators=[DataRequired("You must provide a segment name")])
        author      = StringField(u'Authors', default="Various") 
        prereq      = QuerySelectMultipleField(u'Select Prerequisites for this segment', allow_blank=True, query_factory=lambda: get_elders(segment_id) if segment_id else get_children(course_id), default=lambda: get_prerequisites(segment_id) if segment_id else [], get_pk=lambda item: item.id, get_label=lambda item: item.name, description="Leave blank for no prereq. Use 'Shift' and 'Ctrl/Cmd' for multiple selection/deselection")
        submit      = SubmitField(u'Create/Update Segment')
    return SegmentForm

def _get_quiz_form(segment_id, quiz_id=None):
    class QuizForm(FlaskForm):
        id          = StringField(u'Quiz Id', validators=[])
        name        = StringField(u'Name of Quiz', validators=[DataRequired("You must provide a quiz name")])
        maxscore    = FloatField(u'Total Points', [optional()], description='Maximum Points this Quiz is worth. Leave blank for QuizMaker Points')
        quiz        = FileField(u'Upload Quiz Archive', validators=[FileAllowed(quiz_archive, 'Quiz Archives Only!')])
        prereq      = QuerySelectMultipleField(u'Select Prerequisites for this quiz', allow_blank=True, query_factory=lambda: get_elders(quiz_id) if quiz_id else get_children(segment_id), default=lambda: get_prerequisites(quiz_id) if quiz_id else [], get_pk=lambda item: item.id, get_label=lambda item: item.name, description="Leave blank for no prereq. Use 'Shift' and 'Ctrl/Cmd' for multiple selection/deselection")
        submit      = SubmitField(u'Add/Modify Quiz')
    return QuizForm

def _get_video_form(segment_id, video_id=None):
    class VideoForm(FlaskForm):
        id          = StringField(u'Video Id', validators=[])
        name        = StringField(u'Name of Video', validators=[DataRequired("You must provide a video title")])
        video       = FileField(u'Upload Video', validators=[FileAllowed(video_file, 'Allowed format: mp4, webm')])
        prereq      = QuerySelectMultipleField(u'Select Prerequisites for this video', allow_blank=True, query_factory=lambda: get_elders(video_id) if video_id else get_children(segment_id), default=lambda: get_prerequisites(video_id) if video_id else [], get_pk=lambda item: item.id, get_label=lambda item: item.name, description="Leave blank for no prereq. Use 'Shift' and 'Ctrl/Cmd' for multiple selection/deselection")
        submit      = SubmitField(u'Add/Modify Video')
    return VideoForm

def _get_lecture_form(segment_id, lecture_id=None):
    class LectureForm(FlaskForm):
        id          = StringField(u'Lecture Id', validators=[])
        name        = StringField(u'Name for these Slides', validators=[DataRequired("You must provide a lecture title")])
        lecture     = FileField(u'Upload Lecture File', validators=[FileAllowed(lecture_file, 'Allowed format: ppt, pdf, pptx')])
        prereq      = QuerySelectMultipleField(u'Select Prerequisites for this lecture', allow_blank=True, query_factory=lambda: get_elders(lecture_id) if lecture_id else get_children(segment_id), default=lambda: get_prerequisites(lecture_id) if lecture_id else [], get_pk=lambda item: item.id, get_label=lambda item: item.name, description="Leave blank for no prereq. Use 'Shift' and 'Ctrl/Cmd' for multiple selection/deselection")
        submit      = SubmitField(u'Add/Modify Lecture')
    return LectureForm

class DownloadableForm(FlaskForm):
    id          = StringField(u'ID', validators=[])
    name        = StringField(u'Name of Material:', validators=[DataRequired("You must provide a name")])
    location    = StringField(u'File name:', validators=[DataRequired("You must provide a filename")], description='Enter a filename. Only alphanumericals and underscores allowed')
    asset       = FileField(u'Upload Downloadable Material', validators=[FileAllowed(quiz_archive, 'Archives Only')])
    submit      = SubmitField(u'Add/Modify Material')
