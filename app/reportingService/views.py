from flask import jsonify, session, request, redirect, url_for, render_template, flash
from flask_security import current_user, login_required

from . import stats
from .forms import UserEmailForm, _get_user_name_form
from .controllers import (
        update_video_stats,
        update_lecture_stats,
        _get_all_stats
)
from ..utils import convert_to_uuid, redirect_url, nocache

@login_required
@stats.route('/')
def reporting():
    if not current_user.has_role('admin'):
        return redirect(url_for('core.home'))
    return render_template('report.html')

@login_required
@stats.route('/student/progress', methods=['GET', 'POST'])
def get_progress_by_email():
    if not current_user.has_role('admin'):
        return redirect(url_for('core.home'))
    form = UserEmailForm()
    if form.validate_on_submit():
        return redirect(url_for('core.show_all_user_progress', email=form.email.data))
    return render_template('get_email.html', form=form, head='Get Student Progress')

@login_required
@stats.route('/student/info', methods=['GET', 'POST'])
def get_info_by_email():
    if not current_user.has_role('admin'):
        return redirect(url_for('core.home'))
    form = UserEmailForm()
    if form.validate_on_submit():
        return redirect(url_for('core.edit_profile_admin', email=form.email.data))
    return render_template('get_email.html', form=form, head='Get Student Information')


@login_required
@stats.route('/cert/generate', methods=['GET', 'POST'])
def try_cert_gen():
    if not current_user.has_role('admin'):
        return redirect(url_for('core.home'))
    UserForm = _get_user_name_form()
    form = UserForm()
    if form.validate_on_submit():
        return redirect(url_for('cert.send_cert', course=form.courses.data, name=form.name.data))
    return render_template('get_name.html', form=form, head='Generate Course Certificate')

@stats.route('/courses')
@login_required
def show_course_stats():
    if not current_user.has_role('admin'):
        flash("You do not permission to view this resource")
        return redirect(url_for('core.home'))
    stats = _get_all_stats()
    return render_template('stats.html', stats=stats)

@login_required
@stats.route('/video/update', methods=['POST'])
def video_stats_update():
    duration = float(request.form['duration'])
    newView  = 'new' in request.form
    if 'videoId' not in session:
        response = jsonify({})
        response.status_code = 400
        return response
    videoId = session['videoId']
    update_video_stats(videoId, duration, newView)
    return('', 204)

@login_required
@stats.route('/lecture/update/<id>', methods=['POST'])
def lecture_stats_update(id):
    update_lecture_stats(id)
    return('', 204)


