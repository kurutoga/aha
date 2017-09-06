from .controllers import (
        get_module, get_courses, get_children,
        create_course, create_segment,
        update_course, update_segment,
        delete_course, delete_segment,
        create_quiz, create_video, create_lecture,
        update_quiz, update_video, update_lecture,
        delete_quiz, delete_video, delete_lecture,
        create_course_data, update_course_data,
        delete_course_data, get_course_data,
        get_downloadables, create_downloadable,
        update_downloadable, get_downloadable,
        delete_downloadable, add_prerequisites,
        delete_prereq_requirements
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
        extract_quiz_task, delete_resource, delete_quiz_resource
)
from .forms import (
        _get_course_form, _get_segment_form,
        _get_quiz_form, _get_video_form,
        _get_lecture_form, DownloadableForm
)
from . import repo
from flask_security import current_user, login_required
from flask import redirect, url_for, render_template, request
from wtforms import ValidationError
from . import quiz_archive, video_file, lecture_file, root
from config import Config

BASE_PATH = Config.BASE_PATH

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
    CourseForm = _get_course_form()
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
        add_prerequisites(courseId, form.prereq.data)
        return render_template('segment_repo.html', title=name, course_id=courseId)
    del form.id
    return render_template('aioform.html', form=form, title='Add a course')

@repo.route('/course/<course_id>/edit', methods=['GET', 'POST'])
@login_required
@nocache
def edit_course(course_id):
    if not isAdmin():
        return('', 401)
    CourseForm = _get_course_form(course_id)
    form = CourseForm()
    if form.validate_on_submit():
        update_course(course_id, form.name.data, form.author.data, form.expires.data, form.ready.data)
        update_course_data(course_id, form.description.data, form.expires.data, form.ppercent.data)
        add_prerequisites(course_id, form.prereq.data)
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

@repo.route('/course/<course_id>/delete')
@login_required
def del_course(course_id):
    if not isAdmin():
        return('', 401)
    delete_prereq_requirements(course_id)
    delete_course(course_id)
    return redirect(url_for('repo.show_courses'))

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
    SegmentForm = _get_segment_form(course_id)
    form = SegmentForm()
    if form.validate_on_submit():
        name = form.name.data
        author = form.author.data
        segmentId = create_segment(name, course_id, author)
        create_segment_stats(segmentId)
        add_prerequisites(segmentId, form.prereq.data)
        return redirect(url_for('repo.show_modules', course_id=course_id, segment_id=segmentId))
    del form.id
    return render_template('aioform.html', form=form, course_id=course_id, title=course.name)

@repo.route('/course/<course_id>/segment/<segment_id>/edit', methods=['GET', 'POST'])
@login_required
@nocache
def edit_segment(course_id, segment_id):
    if not isAdmin():
        return('', 401)
    SegmentForm = _get_segment_form(course_id, segment_id)
    form = SegmentForm()
    if form.validate_on_submit():
        update_segment(segment_id, form.name.data, form.author.data)
        add_prerequisites(segment_id, form.prereq.data)
        return redirect(url_for('repo.show_segments', course_id=course_id))
    course      = get_module(course_id)
    segment     = get_module(segment_id)
    form.id.data = segment_id
    form.id.render_kw = {'disabled': 'disabled'}
    form.name.data=segment.name
    form.author.data=segment.author
    return render_template('aioform.html', form=form, course_id=course_id, title=course.name)

@repo.route('/course/<course_id>/segment/<segment_id>/delete')
@login_required
def del_segment(course_id, segment_id):
    if not isAdmin():
        return('', 401)
    delete_prereq_requirements(segment_id)
    delete_segment(segment_id)
    return redirect(url_for('repo.show_segments', course_id=course_id))

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
    QuizForm = _get_quiz_form(segment_id)
    form = QuizForm()
    if form.validate_on_submit():
        qa = form.quiz.data
        if not qa:
            del form.id
            form.quiz.errors.append('You must select a quiz file')
            segment = get_module(segment_id)
            return render_template('aioform.html', form=form, segment_id=segment_id, course_id=course_id, title=segment.name, upload_type='quiz')
        filename = str(uuid.uuid4())
        location = quiz_archive.save(qa, folder=BASE_PATH+'quizzes/', name=filename+'.')
        extract_quiz_task.apply_async(args=[location])
        quiz_id = create_quiz(form.name.data, segment_id, filename)
        if form.maxscore.data:
            create_quiz_stats(quiz_id, form.maxscore.data)
        else:
            create_quiz_stats(quiz_id, None)
        add_prerequisites(quiz_id, form.prereq.data)
        return redirect(url_for('repo.show_modules', course_id=course_id, segment_id=segment_id))
    del form.id
    segment = get_module(segment_id)
    return render_template('aioform.html', form=form, segment_id=segment_id, course_id=course_id, title=segment.name, upload_type='quiz')



@repo.route('/course/<course_id>/segment/<segment_id>/quiz/<quiz_id>/edit', methods=['POST', 'GET'])
@login_required
@nocache
def edit_quiz(course_id, segment_id, quiz_id):
    if not isAdmin():
        return('', 401)
    QuizForm = _get_quiz_form(segment_id, quiz_id)
    form = QuizForm()
    quiz = get_module(quiz_id)
    if form.validate_on_submit():
        qa = form.quiz.data
        if not qa:
            filename = quiz.location
        else:
            filename = str(uuid.uuid4())
            location = quiz_archive.save(qa, folder=BASE_PATH+'quizzes/', name=filename+'.')
            extract_quiz_task.apply_async(args=[location])
            delete_quiz_resource.apply_async(args=[(BASE_PATH+'quizzes/'+quiz.location)])
        _update_quiz_max_score(quiz_id, form.maxscore.data)
        update_quiz(quiz_id, form.name.data, filename)
        add_prerequisites(quiz_id, form.prereq.data)
        return redirect(url_for('repo.show_modules', course_id=course_id, segment_id=segment_id))
    segment = get_module(segment_id)
    form.id.data = quiz_id
    form.id.render_kw = {'disabled':'disabled'}
    form.name.data = quiz.name
    form.maxscore.data = get_quiz_max_score(quiz_id)
    return render_template('aioform.html', form=form, course_id=course_id, segment_id=segment_id, title=segment.name, upload_type='quiz')

@repo.route('/course/<course_id>/segment/<segment_id>/quiz/<quiz_id>/delete')
@login_required
def del_quiz(course_id, segment_id, quiz_id):
    if not isAdmin():
        return('', 401)
    quiz = get_module(quiz_id)
    delete_prereq_requirements(quiz_id)
    delete_quiz_resource.apply_async(args=[BASE_PATH+'quizzes/'+quiz.location])
    delete_quiz(quiz_id)
    return redirect(url_for('repo.show_modules', course_id=course_id, segment_id=segment_id))

@repo.route('/course/<course_id>/segment/<segment_id>/video/new', methods=['GET', 'POST'])
@login_required
@nocache
def add_video(course_id, segment_id):
    if not isAdmin():
        return('', 401)
    VideoForm = _get_video_form(segment_id)
    form = VideoForm()
    if form.validate_on_submit():
        vf = form.video.data
        if not vf:
            return('You must select a video file', 400)
        filename = str(uuid.uuid4())
        location = video_file.save(vf, folder=BASE_PATH+'videos/', name=filename+'.')
        video_id = create_video(form.name.data, segment_id, filename+'.'+vf.filename.split('.')[-1])
        create_video_stats(video_id)
        add_prerequisites(video_id, form.prereq.data)
        return('Success', 200)
    del form.id
    segment = get_module(segment_id)
    return render_template('aioform.html', form=form, segment_id=segment_id, segment=segment, course_id=course_id, title=segment.name, upload_type='video')

@repo.route('/course/<course_id>/segment/<segment_id>/video/<video_id>/edit', methods=['GET', 'POST'])
@login_required
@nocache
def edit_video(course_id, segment_id, video_id):
    if not isAdmin():
        return('', 401)
    VideoForm = _get_video_form(segment_id, video_id)
    form = VideoForm()
    video = get_module(video_id)
    if form.validate_on_submit():
        vf = form.video.data
        if not vf:
            filename = video.location
        else:
            filename = str(uuid.uuid4())
            location = video_file.save(vf, folder=BASE_PATH+'videos/', name=filename+'.')
            filename = filename+'.'+location.split('.')[-1]
            delete_resource.apply_async(args=[BASE_PATH+'videos/'+video.location])
        update_video(video_id, form.name.data, filename)
        add_prerequisites(video_id, form.prereq.data)
        return ('Success', 200)
    segment = get_module(segment_id)
    form.id.data = video_id
    form.id.render_kw = {'disabled':'disabled'}
    form.name.data = video.name
    return render_template('aioform.html', form=form, course_id=course_id, segment_id=segment_id, title=segment.name, upload_type='video')

@repo.route('/course/<course_id>/segment/<segment_id>/video/<video_id>/delete')
@login_required
def del_video(course_id, segment_id, video_id):
    if not isAdmin():
        return('', 401)
    delete_prereq_requirements(video_id)
    video = get_module(video_id)
    location = video.location
    delete_video(video_id)
    delete_resource.apply_async(args=[BASE_PATH+'videos/'+location])
    return redirect(url_for('repo.show_modules', course_id=course_id, segment_id=segment_id))

@repo.route('/course/<course_id>/segment/<segment_id>/lecture/new', methods=['GET', 'POST'])
@login_required
@nocache
def add_lecture(course_id, segment_id):
    if not isAdmin():
        return('', 401)
    LectureForm = _get_lecture_form(segment_id)
    form = LectureForm()
    if form.validate_on_submit():
        lf = form.lecture.data
        if not lf:
            del form.id
            form.lecture.errors.append('You must upload you lectures')
            segment = get_module(segment_id)
            return render_template('aioform.html', form=form, course_id=course_id, segment_id=segment_id, title=segment.name, upload_type='lecture')
        filename = str(uuid.uuid4())
        location = lecture_file.save(lf, folder=BASE_PATH+'lectures/', name=filename+'.')
        lecture_id = create_lecture(form.name.data, segment_id, filename+'.'+lf.filename.split('.')[-1])
        create_lecture_stats(lecture_id)
        add_prerequisites(lecture_id, form.prereq.data)
        return redirect(url_for('repo.show_modules', course_id=course_id, segment_id=segment_id))
    del form.id
    segment = get_module(segment_id)
    return render_template('aioform.html', form=form, segment_id=segment_id, course_id=course_id, title=segment.name, upload_type='lecture')

@repo.route('/course/<course_id>/segment/<segment_id>/lecture/<lecture_id>/edit', methods=['GET', 'POST'])
@login_required
@nocache
def edit_lecture(course_id, segment_id, lecture_id):
    if not isAdmin():
        return('', 401)
    LectureForm = _get_lecture_form(segment_id, lecture_id)
    form = LectureForm()
    lecture = get_module(lecture_id)
    if form.validate_on_submit():
        lf = form.lecture.data
        if not lf:
            filename = lecture.location
        else:
            filename = str(uuid.uuid4())
            location = lecture_file.save(lf, folder=BASE_PATH+'lectures/', name=filename+'.')
            filename = filename+'.'+location.split('.')[-1]
            delete_resource.apply_async(args=[BASE_PATH+'lectures/'+lecture.location])
        update_lecture(lecture_id, form.name.data, filename)
        add_prerequisites(lecture_id, form.prereq.data)
        return redirect(url_for('repo.show_modules', course_id=course_id, segment_id=segment_id))
    segment = get_module(segment_id)
    form.id.data = lecture_id
    form.id.render_kw = {'disabled':'disabled'}
    form.name.data = lecture.name
    return render_template('aioform.html', form=form, course_id=course_id, segment_id=segment_id, title=segment.name, upload_type='lecture')

@repo.route('/course/<course_id>/segment/<segment_id>/lecture/<lecture_id>/delete')
@login_required
def del_lecture(course_id, segment_id, lecture_id):
    if not isAdmin():
        return('', 401)
    lecture = get_module(lecture_id)
    delete_resource.apply_async(args=[BASE_PATH+'lectures/'+lecture.location])
    delete_prereq_requirements(lecture_id)
    delete_lecture(lecture_id)
    return redirect(url_for('repo.show_modules', course_id=course_id, segment_id=segment_id))

@repo.route('/downloadables')
@login_required
@nocache
def show_downloadables():
    if not isAdmin():
        return ('', 401)
    downloadables = get_downloadables()
    return render_template('dwd_repo.html', downloadables=downloadables)


@repo.route('/downloadables/new', methods=['GET', 'POST'])
@login_required
@nocache
def add_downloadable():
    if not isAdmin():
        return('', 401)
    form = DownloadableForm()
    if form.validate_on_submit():
        data = form.asset.data
        if not data:
            del form.id
            form.asset.errors.append('You must upload an archive.')
            return render_template('dwdform.html', form=form)
        filename = form.location.data
        if len(filename.split('.'))==1:
            filename = filename+'.'
        location = quiz_archive.save(data, folder=BASE_PATH+'data/', name=filename)
        location = location.split('/')[-1]
        create_downloadable(form.name.data, location)
        return redirect(url_for('repo.show_downloadables'))
    del form.id
    return render_template('dwdform.html', form=form)

@repo.route('/downloadables/<dwd_id>/edit', methods=['GET', 'POST'])
@login_required
@nocache
def edit_downloadable(dwd_id):
    if not isAdmin():
        return('', 401)
    form = DownloadableForm()
    downloadable = get_downloadable(dwd_id)
    if form.validate_on_submit():
        data = form.asset.data
        if not data:
            location = downloadable.location
        else:
            delete_resource.apply_async(args=[BASE_PATH+'data/'+downloadable.location])
            filename = form.location.data
            if len(filename.split('.'))==1:
                filename=filename+'.'
            location = quiz_archive.save(data, folder=BASE_PATH+'data/', name=filename)
            location = location.split('/')[-1]
        update_downloadable(dwd_id, form.name.data, location)
        return redirect(url_for('repo.show_downloadables'))
    form.id.data = dwd_id
    form.id.render_kw = {'disabled':'disabled'}
    form.name.data = downloadable.name
    form.location.data = downloadable.location
    return render_template('dwdform.html', form=form)

@repo.route('/downloadables/<dwd_id>/delete')
@login_required
def del_downloadable(dwd_id):
    if not isAdmin():
        return('', 401)
    dw = get_downloadable(dwd_id)
    delete_resource.apply_async(args=[BASE_PATH+'data/'+dw.location])
    delete_downloadable(dwd_id)
    return redirect(url_for('repo.show_downloadables'))

