import uuid
import sys

from .models import (
        CourseStats,
        SegmentStats,
        QuizStats,
        VideoStats,
        LectureStats
)
from app import db

'''
base methods to get, create, update 'module' table objects.
'''

def commit():
    try:
        db.session.commit()
    except:
        e = sys.exc_info()[0]
        #TODO: Log
        raise
    return

def create_commit(o):
    db.session.add(o)
    commit()

def get_course_stats(courseId):
    cs = CourseStats.query.get(courseId)
    return cs

def get_segment_stats(segmentId):
    ss = SegmentStats.query.get(segmentId)
    return ss

def get_quiz_stats(quizId):
    qs = QuizStats.query.get(quizId)
    return qs

def get_video_stats(videoId):
    vs = VideoStats.query.get(videoId)
    return vs

def get_lecture_stats(lectureId):
    ls = LectureStats.query.get(lectureId)
    return ls

def create_course_stats(courseId):
    cs = CourseStats(module_id=courseId)
    create_commit(cs)
    return cs.id

def create_segment_stats(segmentId):
    ss = SegmentStas(module_id=segmentId)
    create_commit(ss)
    return ss.id

def create_lecture_stats(lectureId):
    ls = LectureStats(module_id=lectureId)
    create_commit(ls)
    return ls.id

def create_video_stats(videoId):
    vs = VideoStats(module_id=videoId)
    create_commit(vs)
    return vs.id

def create_quiz_stats(quizId, segmentId, courseId, maxScore):
    qs = QuizStats(module_id=quizId)
    qs.max_score = maxScore
    db.session.add(qs)
    commit()
    return qs.id

def update_quiz_stats_add_attempt(quizId, segmentId, courseId, awardedPercent, duration):
    qs = get_quiz_stats(quizId)
    qs.avg_score = awardedPercent * qs.max_score
    qs.duration += duration
    commit()

def update_lecture_stats(lectureId):
    ls = get_lecture_stats(lectureId)
    ls.downloads+=1
    commit()

def update_video_stats(videoId, duration, newView=False):
    vs = get_video_stats(videoId)
    if newView:
        vs.views+=1
    vs.duration+=duration
    commit()

def _update_segment_enroll(segmentId):
    ss = get_segment_stats(segmentId)
    ss.current_students+=1

def _update_segment_student_finish(segmentId):
    ss = get_segment_stats(segmentId)
    ss.students += 1
    ss.current_students -=1

def _update_course_student_finish(courseId):
    cs = get_course_stats(courseId)
    cs.current_students -= 1
    cs.students += 1

def _update_course_enroll(courseId):
    cs = get_course_stats(courseId)
    cs.current_students += 1
