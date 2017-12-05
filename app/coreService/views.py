from flask import render_template, jsonify, url_for, request, redirect, flash, send_from_directory, session, make_response
from flask_security import login_required, current_user
from .forms import UserEditForm, UserVerifyForm

from . import core
from .controllers import (
        _get_module, _get_status, _get_segment_and_module_status,
        _get_courses_and_status, _get_courses,
        _get_next_mod, _get_prev_mod, _get_type, _get_course_data,
        update_user_profile, _get_progress, _get_downloadable,
        _get_downloadables, confirm_user_email, get_user_by_email, _get_all_progress
)
from ..utils import convert_to_uuid, redirect_url, nocache, _get_now
from config import Config

BASE_PATH = Config.BASE_PATH

@core.route('/')
@core.route('dashboard')
@nocache
def home():
    if not current_user.is_authenticated:
        courses = _get_courses()
        return render_template('home.html', courses=courses)
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
@nocache
def course(id):
    course = _get_module(id)
    userId = current_user.id
    session['userId']=userId
    if not course or course.type!='course':
        flash("Invalid Course ID")
        redirect(redirect_url())
    status   = _get_status(course.id, userId)
    if not status:
        courseData = _get_course_data(course.id)
        session['courseId']=id
        return render_template("course_enroll.html", course=course, courseData=courseData)
    segments = _get_segment_and_module_status(course.id, userId)
    cdata     = _get_course_data(course.id)
    return render_template("course.html", segments=segments, course=course, courseStatus=status, vidlink=cdata.video_link)

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

@core.route('video/get/<loc>')
@login_required
def get_video(loc):
    return send_from_directory(BASE_PATH+'videos', loc)

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
    return send_from_directory(BASE_PATH+'lectures', lecture.location, as_attachment=True, attachment_filename=lecture.name+'.'+lecture.location.split('.')[-1])


@core.route('quiz/<id>')
@login_required
def quiz(id):
    quiz = _get_module(id)
    userId = current_user.id
    userName = current_user.name
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
        return redirect(url_for('core.course', id=segment.parent))
    session['quizId']=quiz.id
    session['segmentId']=segment.id
    session['courseId']=segment.parent
    session['userId']=userId
    session['quizLocation']=quiz.location
    session['userName']=userName
    session.modified = True
    return render_template('quiz.html', quiz=quiz, segment=segment)

@core.route('quizzes/{{location}}')
@login_required
def quizLoad(location):
    if 'userId' not in session or current_user.id!=session['userId'] or 'quizLocation' not in session or location!=session['quizLocation']:
        flash("You session may have expired")
        return redirect(redirect_url())
    print(session['quizLocation'])
    return send_from_directory(BASE_PATH+'quizzes/'+session['quizLocation'], 'index.html')

@core.route('quizzes/{{location}}/data/<file>')
@login_required
def quizAssest(file):
    return send_from_directory(BASE_PATH+'quizzes/'+session['quizLocation']+'/data/', file)

@core.route('dw')
@login_required
def downloadables():
    downloadables = _get_downloadables()
    return render_template('downloadables.html', downloadables=downloadables)

@core.route('dw/<dwd_id>')
@login_required
def download_material(dwd_id):
    dwd = _get_downloadable(dwd_id)
    return send_from_directory(BASE_PATH+'data', dwd.location, as_attachment=True, attachment_filename=dwd.location)

@core.route('user/edit', methods=['POST', 'GET'])
@login_required
def edit_profile():
    userId = current_user.id
    form = UserEditForm()
    if form.validate_on_submit():
        update_user_profile(userId, form.name.data, form.nickname.data, form.sex.data, form.city.data, \
                             form.state.data, form.country.data, form.nationality.data, form.occupation.data)
        return redirect(url_for('core.home'))
    form.name.data = current_user.name
    form.nickname.data = current_user.nickname
    form.sex.data = current_user.sex
    form.city.data = current_user.city
    form.state.data = current_user.state
    form.country.data = current_user.country
    form.nationality.data = current_user.nationality
    form.occupation.data = current_user.occupation
    return render_template('edit_user.html', form=form)

@core.route('user/info/<email>', methods=['POST', 'GET'])
@login_required
def edit_profile_admin(email):
    if not current_user.has_role('admin'):
        flash("Error. You do not have the permission to view this resource")
        return redirect(url_for('core.home'))
    user = get_user_by_email(email)
    if not user:
        flash("Error. Invalid email provided.")
        return redirect(url_for('core.home'))
    userId = user.id
    form = UserEditForm()
    if form.validate_on_submit():
        update_user_profile(userId, form.name.data, form.nickname.data, form.sex.data, form.city.data, \
                             form.state.data, form.country.data, form.nationality.data, form.occupation.data)
        return redirect(url_for('stats.reporting'))
    form.name.data = user.name
    form.nickname.data = user.nickname
    form.sex.data = user.sex
    form.city.data = user.city
    form.state.data = user.state
    form.country.data = user.country
    form.nationality.data = user.nationality
    form.occupation.data = user.occupation
    return render_template('edit_user_admin.html', form=form)

@core.route('user/scores')
@login_required
def show_user_progress():
    userId = current_user.id
    progress = _get_progress(userId)
    return render_template('show_progress.html', progress=progress)

@core.route('user/allscores/<email>')
@login_required
def show_all_user_progress(email):
    if not current_user.has_role('admin'):
        flash("You do not permission to view this resource")
        return redirect(url_for('core.home'))
    user = get_user_by_email(email)
    if not user:
        flash("(ERROR) Invalid Email Address.")
        return redirect(url_for('core.home'))
    progress = _get_all_progress(user.id)
    return render_template('progress.html', progress=progress, name=user.name)

@core.route('student/verify', methods=['POST', 'GET'])
@login_required
def verify_student():
    if not current_user.has_role('admin'):
        return redirect(url_for('core.home'))
    form = UserVerifyForm()
    if form.validate_on_submit():
        success = confirm_user_email(form.email.data)
        if not success:
            flash("Error Verifying Email Address. Invalid Email")
            return redirect(url_for('core.home'))
        flash("success")
        return redirect(url_for('core.home'))
    return render_template('verify.html', verify_user_form=form)
