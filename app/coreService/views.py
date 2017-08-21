from flask import render_template, jsonify, url_for, request, redirect, flash, send_from_directory, session
from flask_security import login_required, current_user

from . import core
from .controllers import (
        _get_module, _get_status, _get_segment_and_module_status,
        _get_courses_and_status, _get_courses,
        _get_next_mod, _get_prev_mod, _get_type, _get_course_data
)
from ..utils import convert_to_uuid, redirect_url, nocache, _get_now

@core.route('/')
@core.route('dashboard')
def home():
    if not current_user.is_authenticated:
        return render_template('home.html')
    if current_user.has_role('admin'):
        return render_template('admin.html')
    available, inprogress, completed = _get_courses_and_status(current_user.id)
    return render_template('dash.html', available=available, inprogress=inprogress, completed=completed)

@core.route('resource/<id>/next')
@login_required
def next_module(id):
    mod = _get_next_mod(id)
    if mod:
        if mod.type=='lecture':
            return redirect(url_for('core.next_module', id=mod.parent))
        return redirect(url_for('core.'+mod.type, id=mod.id))
    flash("Invalid Enpoint")
    return redirect(redirect_url())

@core.route('resource/<id>/prev')
@login_required
def prev_module(id):
    mod = _get_prev_mod(id)
    if mod:
        if mod.type=='lecture':
            return redirect(url_for('core.prev_module', id=mod.parent))
        return redirect(url_for('core.'+mod.type, id=mod.id))
    flash("Invalid Enpoint")
    return redirect(redirect_url())

@core.route('segment/<id>')
@login_required
def segment(id):
    segment = _get_module(id)
    if not segment or segment.type!='segment':
        flash("Invalid Endpoint")
        return redirect(redirect_url())
    return redirect(url_for('core.course', id=segment.parent))

@core.route('course/<id>')
@login_required
def course(id):
    course = _get_module(id)
    userId = current_user.id
    if not course or course.type!='course':
        flash("Invalid Course ID")
        redirect(redirect_url())
    status   = _get_status(course.id, userId)
    if not status:
        courseData = _get_course_data(course.id)
        session['courseId']=id
        session['userId']=userId
        return render_template("course_enroll.html", course=course, courseData=courseData)
    segments = _get_segment_and_module_status(course.id, userId)
    return render_template("course.html", segments=segments, course=course, courseStatus=status)

@core.route('video/<id>')
@login_required
def video(id):
    video = _get_module(id)
    userId = current_user.id
    if not video or video.type!='video':
        flash("invalid URL")
        return redirect(redirect_url())
    segstatus = _get_status(video.parent, userId)
    if not segstatus:
        flash("You are not enrolled in this class")
        return redirect(redirect_url())
    status = _get_status(video.id, userId)
    segment = _get_module(video.parent)
    session['videoId']=video.id
    session['userId']=userId
    return render_template('video.html', video=video, segment=segment, status=status)

@core.route('video/frame/<loc>')
@login_required
def video_frame(loc):
    duration = request.args.get('duration', 0, type=int)
    return render_template('vid-frame.html', location=loc, duration=duration)

@core.route('lecture/<id>')
@login_required
def lecture(id):
    lecture = _get_module(id)
    userId  = current_user.id
    if not lecture or lecture.type!='lecture':
        flash("invalid URL")
        return redirect(redirect_url())
    segstatus = _get_status(lecture.parent, userId)
    if not segstatus:
        flash("You are not enrolled in this class")
        return redirect(redirect_url())
    status = _get_status(lecture.id, userId)
    segment = _get_module(lecture.parent)
    session['lectureId']=lecture.id
    session['userId']=userId
    return send_from_directory('lectures/'+str(id), lecture.location, as_attachment=True)


@core.route('quiz/<id>')
@login_required
@nocache
def quiz(id):
    quiz = _get_module(id)
    userId = current_user.id
    if not quiz or quiz.type!='quiz':
        flash("Invalid Quiz URL")
        return redirect(redirect_url())
    segstatus = _get_status(quiz.parent, userId)
    if not segstatus:
        flash("You are not enrolled in this class")
        return redirect(redirect_url())
    segment = _get_module(quiz.parent)
    qstatus = _get_status(quiz.id, userId)
    if qstatus:
        return redirect(url_for('core.course', segment.parent))
    session['quizId']=quiz.id
    session['segmentId']=segment.id
    session['courseId']=segment.parent
    session['userId']=userId
    return render_template('quiz.html', quiz=quiz, segment=segment)

@core.route('quizzes/<int:userid>/<base>/')
@login_required
@nocache
def quizLoad(userid, base):
    if current_user.id != userid:
        flash("Invalid User")
        return redirect(redirect_url())
    return send_from_directory('quizzes/'+base, 'index.html')

@core.route('quizzes/<userid>/<base>/data/<file>')
@login_required
@nocache
def quizAssest(userid, base, file):
    return send_from_directory('quizzes/'+base+'/data/', file)

