import xmltodict
from flask import jsonify, session, request, Response, json
from flask_security import login_required, current_user

from . import progress
from .tasks import (
        quiz_scoring_task
)
from .controllers import (
        create_course_progress,
        create_quiz_progress,
        create_update_video_progress,
        create_update_lecture_progress,
        start_quiz,
        get_quiz_detailed_result
)
from ..utils import convert_to_uuid, redirect_url, nocache

@progress.route('/course/enroll', methods=['POST'])
@login_required
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
@login_required
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
@login_required
def update_lecture_progress(id):
    if 'userId' not in session:
        return ('', 400)
    userId = session['userId']
    create_update_lecture_progress(id, userId)
    return ('', 204)

@progress.route('/quizxml/<id>')
@login_required
def get_quizxml(id):
    injson = request.args.get("json")
    if not current_user.has_role('admin'):
        return ('Unauthorized', 401)
    qxml = get_quiz_detailed_result(id)
    if not qxml:
        return ('Not Found', 404)
    if injson:
        return Response(json.dumps(xmltodict.parse(qxml.quizxml)), mimetype='application/json', headers={'Content-Disposition':'attachment;filename=result.json'})
    return Response(qxml.quizxml, mimetype='application/text', headers={'Content-Disposition': 'attachment;filename=result.xml'})

@progress.route('/quiz/new', methods=['POST'])
@login_required
def update_quiz_progress():
    if 'quizId' not in session or 'segmentId' not in session or \
            'courseId' not in session or 'userId' not in session or \
            'userName' not in session:
        return('', 400)

    userId = session['userId']
    segmentId = session['segmentId']
    courseId = session['courseId']
    quizId = session['quizId']
    userName = session['userName']

    ap = float(request.form['sp'])
    pp = float(request.form['ps'])
    psp = float(request.form['psp'])
    tp = float(request.form['tp'])
    dr = request.form['dr']
    awp = (ap/tp)*100
    ut = float(request.form['ut'])
    quiz_scoring_task.apply_async(args=[quizId, segmentId, courseId, userId, userName, pp, ap, psp, awp, tp, ut, dr])

    del session['courseId']
    del session['quizId']
    del session['segmentId']
    del session['userId']
    del session['userName']
    del session['quizLocation']
    return ('', 200)

@progress.route('/quiz/start', methods=['POST'])
@login_required
def begin_quiz():
    if 'quizId' not in session or 'userId' not in session:
        return('', 400)

    userId = session['userId']
    quizId = session['quizId']
    start_quiz(quizId, userId)
    return ('', 200)
