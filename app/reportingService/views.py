from flask import jsonify, session, request

from . import stats
from .controllers import (
        update_video_stats,
        update_lecture_stats
)
from ..utils import convert_to_uuid, redirect_url, nocache

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

@stats.route('/lecture/update/<id>', methods=['POST'])
def lecture_stats_update(id):
    update_lecture_stats(id)
    return('', 204)


