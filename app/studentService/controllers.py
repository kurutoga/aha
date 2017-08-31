'''
    Student Service Controller
    Controller for Student Progress Service.
    Manages Quiz Scores, Video/Lecture Progress and Class Status
'''

import uuid
import sys

from .models import (
        CourseProgress, 
        SegmentProgress, 
        QuizProgress,
        VideoProgress, 
        LectureProgress
)
from app.classService.controllers import get_module, get_total_children, get_expiry_by_id, get_courses
from app.reportingService.controllers import (
        _update_segment_enroll, _update_course_enroll,
        _update_segment_student_finish, _update_course_student_finish,
        _update_quiz_stats_add_attempt, get_quiz_max_score,
        _update_quiz_max_score
)
from app.certService.controllers import create_certificate_pending
from app.utils import add_years, _get_now, add_days
from app       import db


'''
base methods for CRUD operations on models
'''
def commit():
    try:
        db.session.commit()
    except:
        e = sys.exc_info()[0]
        #log
        raise
    return


'''
ClassProgress Methods
'''
def get_course_progress(courseId, userId):
    cp = CourseProgress.query.get([courseId, userId])
    return cp

def get_segment_progress(segmentId, userId):
    sp = SegmentProgress.query.get([segmentId, userId])
    return sp

def get_video_progress(videoId, userId):
    vp = VideoProgress.query.get([videoId, userId])
    return vp

def get_lecture_progress(lectureId, userId):
    lp = LectureProgress.query.get([lectureId, userId])
    return lp

def get_quiz_progress(quizId, userId):
    qp = QuizProgress.query.get([quizId, userId])
    return qp

def get_children_progress(siblings, userId):
    d = []
    for child in siblings:
        if child.type=='quiz':
            qp = get_quiz_progress(child.id, userId)
            d.append(qp)
        elif child.type=='lecture':
            lp = get_lecture_progress(child.id, userId)
            d.append(lp)
        elif child.type=='video':
            vp = get_video_progress(child.id, userId)
            d.append(vp)
        elif child.type=='course':
            cp = get_course_progress(child.id, userId)
            d.append(cp)
        elif child.type=='segment':
            sp = get_segment_progress(child.id, userId)
        else:
            d.append(None)
    return d


# update class by changing completed_segments by segmentDelta parameter.

# data field has no use currently. to store comments location information
def _update_course_progress(courseId, userId, segmentDelta, totalDelta, scoreDelta):
    courseProgress                       = get_course_progress(courseId, userId)
    courseProgress.completed_segments   += segmentDelta
    courseProgress.total_points         += totalDelta
    courseProgress.scored_points        += scoreDelta
    
    totalSegments = get_total_children(courseId)
    if totalSegments <= courseProgress.completed_segments:
        print("###################### WOOOT! GENERATED CERT ################################")
        rt = create_certificate_pending(courseId, userId, courseProgress.scored_points, courseProgress.total_points)
        print(rt)
        courseProgress.completed_at = _get_now()
        courseProgress.is_complete  = True
        _update_course_student_finish(courseId)

def _update_segment_progress(segmentId, courseId, userId, moduleDelta, totalDelta, scoreDelta):
    segmentProgress = get_segment_progress(segmentId, userId)
    segmentProgress.completed_modules   += moduleDelta
    segmentProgress.total_points        += totalDelta
    segmentProgress.scored_points       += scoreDelta
    
    totalModules = get_total_children(segmentId)
    segmentDelta = 0
    if totalModules <= segmentProgress.completed_modules:
        segmentProgress.completed_at = _get_now()
        segmentProgress.is_complete  = True
        segmentDelta = 1
        _update_segment_student_finish(segmentId)
    _update_course_progress(courseId, userId, segmentDelta, totalDelta, scoreDelta)

def _create_segment_progress(segmentId, userId, expires_at):
    sp = SegmentProgress(module_id=segmentId, user_id=userId, expires_at=expires_at, completed_modules=0)
    db.session.add(sp)
    return sp

def get_or_create_segment_progress(segmentId, courseId, userId):
    sp = get_segment_progress(segmentId, userId)
    if not sp:
        cp = get_course_progress(courseId, userId)
        if not cp:
            return None
        sp = _create_segment_progress(segmentId, userId, cp.expires_at)
        _update_segment_enroll(segmentId)
        commit()
    return sp

def create_course_progress(courseId, userId):
    course = get_module(courseId)
    expireDays = get_expiry_by_id(courseId)
    if expireDays:
        dt = add_days(_get_now(), expireDays)
    else:
        dt = add_years(_get_now())
    cp = CourseProgress(module_id=courseId, user_id=userId, expires_at=dt, completed_segments=0)
    _update_course_enroll(courseId)
    db.session.add(cp)
    commit()

def create_quiz_progress(quizId, segmentId, courseId, userId, ppoints, apoints, ppercent, apercent, tpoints, duration):
    sp = get_segment_progress(segmentId, userId)
    if not sp:
        return False
    currentDT = _get_now()
    if sp.expires_at < currentDT:
        return
    max_score = get_quiz_max_score(quizId)
    if not max_score:
        print('we good')
        _update_quiz_max_score(quizId, tpoints)
        max_score = tpoints
    quiz_progress = QuizProgress(
            module_id=quizId, user_id=userId, completed_at=currentDT,
            passing_points = ppoints, awarded_points = apoints,
            passing_percent = ppercent, awarded_percent = apercent,
            total_points=tpoints, duration = duration, is_complete=True
    )
    db.session.add(quiz_progress)
    awarded = (max_score*apercent)/100.00
    _update_quiz_stats_add_attempt(quizId, awarded, duration)
    _update_segment_progress(segmentId, courseId, userId, 1, max_score, awarded)
    commit()

def create_update_video_progress(videoId, userId, time, newView=False):
    videoProgress = get_video_progress(videoId, userId)
    if not videoProgress:
        videoProgress = VideoProgress(module_id=videoId, user_id=userId, duration=0, views=0)
        db.session.add(videoProgress)
    if time>videoProgress.duration:
        videoProgress.duration  = time
    if newView:
        videoProgress.views     += 1
    commit()

def create_update_lecture_progress(lectureId, userId):
    lectureProgress = get_lecture_progress(lectureId, userId)
    if not lectureProgress:
        lectureProgress = LectureProgress(module_id=lectureId, user_id=userId, downloads=0)
        db.session.add(lectureProgress)
    lectureProgress.downloads    += 1
    commit()


'''
TODO: ADD DELETE ENDPOINTS TO SUPPORT UN-ENROLL
'''
