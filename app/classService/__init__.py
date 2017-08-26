from flask import Blueprint
from flask_uploads import UploadSet, ARCHIVES, configure_uploads

quiz_archive = UploadSet('quizzes', extensions=('zip'))
video_file   = UploadSet('videos', extensions=('mp4', 'webm'))
lecture_file = UploadSet('lectures', extensions=('pdf', 'pptx', 'ppt'))
root         = ''

repo = Blueprint('repo', __name__, url_prefix='/repo')

from . import views

def configure_up(app):
    configure_uploads(app, (quiz_archive, video_file, lecture_file))
    root = app.instance_path
    print(app.instance_path)
