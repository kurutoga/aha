from .controllers import (
        get_module, get_courses, get_children,
        create_course, create_segment,
        update_course, update_segment,
        delete_course, delete_segment,
        create_quiz, create_video, create_lecture,
        update_quiz, update_video, update_lecture,
        delete_quiz, delete_video, delete_lecture,
        create_course_data, update_course_data,
        delete_course_data, get_course_data
)

from app.reportingService.controllers import (
        create_course_stats, create_segment_stats,
        create_video_stats, create_quiz_stats,
        create_lecture_stats, get_quiz_max_score,
        _update_quiz_max_score
)
from ..utils import convert_to_uuid, redirect_url, nocache, _get_now
import uuid
from .tasks import (
        extract_quiz_task
)
from .forms import (
        CourseForm, SegmentForm,
        VideoForm, QuizForm,
        LectureForm
)
from . import repo
from flask_security import current_user, login_required
from flask import redirect, url_for, render_template, request
from wtforms import ValidationError
from . import quiz_archive, video_file, lecture_file, root

BASE_PATH = '/home/bishu/Projects/aha/app/'

def isAdmin():
    if current_user.has_role('admin'):
        return True
    return False

@repo.route('/courses')
@login_required
@nocache
def show_courses():
    if not isAdmin():
        return ('', 401)
    courses = get_courses()
    return render_template('course_repo.html', courses=courses)

@repo.route('/courses/new', methods=['GET', 'POST'])
@login_required
@nocache
def add_course():
    if not isAdmin():
        return ('', 401)
    form = CourseForm()
    if form.validate_on_submit():
        name = form.name.data
        author = form.author.data
        desc = form.description.data
        duration = form.expires.data
        passpercent = form.ppercent.data
        is_ready = form.ready.data
        courseId = create_course(name, author, duration, None, is_ready)
        if not courseId:
            raise ValidationError("Could not create Course " + name)
        create_course_data(courseId, desc, duration, passpercent)
        create_course_stats(courseId)
        return render_template('segment_repo.html', title=name, course_id=courseId)
    del form.id
    return render_template('aioform.html', form=form, title='Course Repository')

@repo.route('/course/<course_id>/edit', methods=['GET', 'POST'])
@login_required
@nocache
def edit_course(course_id):
    if not isAdmin():
        return('', 401)
    form = CourseForm()
    if form.validate_on_submit():
        update_course(form.id.data, form.name.data, form.author.data, form.duration.data, form.is_ready.data)
        update_course_data(form.id.data, form.description.data, form.duration.data, form.ppercent.data)
        return redirect(url_for('repo.show_courses'))
    course      = get_module(course_id)
    course_data = get_course_data(course_id)
    form.id.data = course_id
    form.id.render_kw = {'disabled': 'disabled'}
    form.name.data=course.name
    form.author.data=course.author
    form.expires.data = course_data.duration_weeks
    form.description.data = course_data.description
    form.ready.data = course.is_ready
    form.ppercent.data = course_data.pass_percent
    return render_template('aioform.html', form=form, title='Course Repository')

@repo.route('/course/<course_id>/segments')
@login_required
@nocache
def show_segments(course_id):
    if not isAdmin():
        return('', 401)
    segments = get_children(course_id)
    return render_template('segment_repo.html', segments=segments, course_id=course_id)
    
@repo.route('/course/<course_id>/segments/new', methods=['GET', 'POST'])
@login_required
@nocache
def add_segment(course_id):
    if not isAdmin():
        return('', 401)
    course = get_module(course_id)
    form = SegmentForm()
    if form.validate_on_submit():
        name = form.name.data
        author = form.author.data
        segmentId = create_segment(name, course_id, author)
        create_segment_stats(segmentId)
        return redirect(url_for('repo.show_modules', course_id=course_id, segment_id=segmentId))
    del form.id
    return render_template('aioform.html', form=form, course_id=course_id, title=course.name)


@repo.route('/course/<course_id>/segment/<segment_id>/edit', methods=['GET', 'POST'])
@login_required
@nocache
def edit_segment(course_id, segment_id):
    if not isAdmin():
        return('', 401)
    form = SegmentForm()
    if form.validate_on_submit():
        update_segment(form.id.data, form.name.data, form.author.data)
        return redirect(url_for('repo.show_segments', course_id=course_id))
    course      = get_module(course_id)
    segment     = get_module(segment_id)
    form.id.data = segment_id
    form.id.render_kw = {'disabled': 'disabled'}
    form.name.data=segment.name
    form.author.data=segment.author
    form.required.data = segment.is_ready
    return render_template('aioform.html', form=form, course_id=course_id, title=course.name)

@repo.route('/course/<course_id>/segment/<segment_id>/modules')
@login_required
@nocache
def show_modules(course_id, segment_id):
    if not isAdmin():
        return('', 401)
    modules = get_children(segment_id)
    segment = get_module(segment_id)
    return render_template('module_repo.html', modules=modules, course_id=course_id, segment_id=segment_id, segment=segment)

@repo.route('/course/<course_id>/segment/<segment_id>/quiz/new', methods=['GET', 'POST'])
@login_required
@nocache
def add_quiz(course_id, segment_id):
    if not isAdmin():
        return('', 401)
    form = QuizForm()
    if form.validate_on_submit():
        qa = form.quiz.data
        print(qa)
        if not qa:
            raise ValidationError("Must Upload Quiz Archive")
        filename = str(uuid.uuid4())
        location = quiz_archive.save(qa, folder=BASE_PATH+'resources/quizzes/', name=filename+'.')
        extract_quiz_task.apply_async(args=[location])
        quiz_id = create_quiz(form.name.data, segment_id, filename)
        create_quiz_stats(quiz_id, form.maxscore.data)
        return redirect(url_for('repo.show_modules', course_id=course_id, segment_id=segment_id))
    del form.id
    segment = get_module(segment_id)
    return render_template('aioform.html', form=form, segment_id=segment_id, course_id=course_id, title=segment.name)



@repo.route('/course/<course_id>/segment/<segment_id>/quiz/<quiz_id>/edit')
@login_required
@nocache
def edit_quiz(course_id, segment_id, quiz_id):
    if not isAdmin():
        return('', 401)
    form = QuizForm()
    if form.validate_on_submit():
        qa = form.quiz.data
        if not qa:
            location = None
        else:
            filename = str(uuid.uuid4())
            location = quiz_archive.save(qa, folder=BASE_PATH+'resources/quizzes/', name=filename+'.')
            extract_quiz_task.apply_async(args=[location])
        _update_quiz_max_score(form.id.data, form.maxscore.data)
        update_quiz(form.id.data, form.name.data, location)
        return redirect(url_for('repo.show_modules', course_id=course_id, segment_id=segment_id))
    quiz = get_module(quiz_id)
    segment = get_module(segment_id)
    form.id.data = quiz_id
    form.id.render_kw = {'disabled':'disabled'}
    form.name.data = quiz.name
    form.required.data = quiz.is_ready
    return render_template('aioform.html', form=form, course_id=course_id, segment_id=segment_id, title=segment.name)

@repo.route('/course/<course_id>/segment/<segment_id>/video/new', methods=['GET', 'POST'])
@login_required
@nocache
def add_video(course_id, segment_id):
    if not isAdmin():
        return('', 401)
    form = VideoForm()
    if form.validate_on_submit():
        vf = form.video.data
        if not vf:
            raise ValidationError("Must Upload A Video File")
        filename = str(uuid.uuid4())
        location = video_file.save(vf, folder=BASE_PATH+'static/videos/', name=filename+'.')
        video_id = create_video(form.name.data, segment_id, filename+'.'+vf.filename.split('.')[-1])
        create_video_stats(video_id)
        return redirect(url_for('repo.show_modules', course_id=course_id, segment_id=segment_id))
    del form.id
    segment = get_module(segment_id)
    return render_template('aioform.html', form=form, segment_id=segment_id, segment=segment, course_id=course_id, title=segment.name)

@repo.route('/course/<course_id>/segment/<segment_id>/video/<video_id>/edit')
@login_required
@nocache
def edit_video(course_id, segment_id, video_id):
    if not isAdmin():
        return('', 401)
    form = VideoForm()
    if form.validate_on_submit():
        vf = form.video.data
        if not vf:
            location = None
        else:
            filename = str(uuid.uuid4())
            location = video_file.save(vf, folder=BASE_PATH+'static/videos/', name=filename+'.')
            location = location.split('/')[-1]
        update_video(form.id.data, form.name.data, location)
        return redirect(url_for('repo.show_modules', course_id=course_id, segment_id=segment_id))
    video = get_module(video_id)
    segment = get_module(segment_id)
    form.id.data = video_id
    form.id.render_kw = {'disabled':'disabled'}
    form.name.data = video.name
    form.required.data = video.is_ready
    return render_template('aioform.html', form=form, course_id=course_id, segment_id=segment_id, title=segment.name)

@repo.route('/course/<course_id>/segment/<segment_id>/lecture/new', methods=['GET', 'POST'])
@login_required
@nocache
def add_lecture(course_id, segment_id):
    if not isAdmin():
        return('', 401)
    form = LectureForm()
    if form.validate_on_submit():
        lf = form.lecture.data
        if not lf:
            raise ValidationError("Must Upload A Lecture File")
        filename = str(uuid.uuid4())
        location = lecture_file.save(lf, folder=BASE_PATH+'resources/lectures/', name=filename+'.')
        lecture_id = create_lecture(form.name.data, segment_id, filename+'.'+lf.filename.split('.')[-1])
        create_lecture_stats(lecture_id)
        return redirect(url_for('repo.show_modules', course_id=course_id, segment_id=segment_id))
    del form.id
    segment = get_module(segment_id)
    return render_template('aioform.html', form=form, segment_id=segment_id, course_id=course_id, title=segment.name)

@repo.route('/course/<course_id>/segment/<segment_id>/lecture/<lecture_id>/edit')
@login_required
@nocache
def edit_lecture(course_id, segment_id, lecture_id):
    if not isAdmin():
        return('', 401)
    form = VideoForm()
    if form.validate_on_submit():
        lf = form.lecture.data
        if not lf:
            location = None
        else:
            filename = str(uuid.uuid4())
            location = lecture_file.save(lf, folder=BASE_PATH+'resources/lectures/', name=filename+'.')
            location = location.split('/')[-1]
        update_lecture(form.id.data, form.name.data, location)
        return redirect(url_for('repo.show_modules', course_id=course_id, segment_id=segment_id))
    lecture = get_module(lecture_id)
    segment = get_module(segment_id)
    form.id.data = lecture_id
    form.id.render_kw = {'disabled':'disabled'}
    form.name.data = lecture.name
    form.required.data = lecture.is_ready
    return render_template('aioform.html', form=form, course_id=course_id, segment_id=segment_id, title=segment.name)


