from flask import jsonify, session, request

from . import progress
from .tasks import (
        quiz_scoring_task
)
from .controllers import (
        create_course_progress,
        create_quiz_progress,
        create_update_video_progress,
        create_update_lecture_progress
)
from ..utils import convert_to_uuid, redirect_url, nocache

@progress.route('/course/enroll', methods=['POST'])
def enroll():
    if 'courseId' not in session or 'userId' not in session:
        response = jsonify({})
        response.status_code = 400
        return response
    courseId = session['courseId']
    userId = session['userId']
    create_course_progress(courseId, userId)
    response = jsonify({'id':courseId})
    response.status_code = 200
    del session['courseId']
    del session['userId']
    return response

@progress.route('/video/update', methods=['POST'])
def update_video_progress():
    duration = float(request.form['duration'])
    newView  = 'new' in request.form
    if 'videoId' not in session or 'userId' not in session:
        response = jsonify({})
        response.status_code = 400
        return response
    videoId = session['videoId']
    userId = session['userId']
    create_update_video_progress(videoId, userId, duration, newView)
    return('', 204)

@progress.route('/lecture/update/<id>', methods=['POST'])
def update_lecture_progress(id):
    if 'userId' not in session:
        return ('', 400)
    userId = session['userId']
    create_update_lecture_progress(id, userId)
    return ('', 204)

@progress.route('/quiz/new', methods=['POST'])
def update_quiz_progress():
    if 'quizId' not in session or 'segmentId' not in session or \
            'courseId' not in session or 'userId' not in session:
        return('', 400)

    userId = session['userId']
    segmentId = session['segmentId']
    courseId = session['courseId']
    quizId = session['quizId']

    ap = float(request.form['sp'])
    pp = float(request.form['ps'])
    psp = float(request.form['psp'])
    tp = float(request.form['tp'])
    awp = (ap/tp)*100
    ut = float(request.form['ut'])
    quiz_scoring_task.apply_async(args=[quizId, segmentId, courseId, userId, pp, ap, psp, awp, tp, ut])

    del session['courseId']
    del session['quizId']
    del session['segmentId']
    del session['userId']
    return ('', 200)
