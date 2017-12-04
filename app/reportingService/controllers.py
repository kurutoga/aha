import uuid
import sys

from app.utils import _get_now
from app.classService.controllers import get_courses, get_children

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

def get_quiz_max_score(quizId):
    score = QuizStats.query.with_entities(QuizStats.max_score).filter(QuizStats.module_id==quizId).scalar()
    return score

def create_course_stats(courseId):
    cs = CourseStats(module_id=courseId)
    create_commit(cs)

def create_segment_stats(segmentId):
    ss = SegmentStats(module_id=segmentId)
    create_commit(ss)

def create_lecture_stats(lectureId):
    ls = LectureStats(module_id=lectureId)
    create_commit(ls)

def create_video_stats(videoId):
    vs = VideoStats(module_id=videoId)
    create_commit(vs)

def create_quiz_stats(quizId, maxScore):
    qs = QuizStats(module_id=quizId, max_score=maxScore)
    db.session.add(qs)
    commit()

def _update_quiz_max_score(quizId, score):
    qs = get_quiz_stats(quizId)
    qs.max_score=score

def _update_quiz_stats_add_attempt(quizId, awardedPoints, duration):
    qs = get_quiz_stats(quizId)
    score = qs.attempts*qs.avg_score
    qs.avg_score = (score + awardedPoints)/(qs.attempts+1)
    qs.attempts += 1
    qs.duration += duration

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

def _get_all_stats():
    courses = get_courses()
    res = []
    for course in courses:
        cp = get_course_stats(course.id)
        if cp:
            segments=get_children(course.id)
            course.__dict__['stats']=cp
            course.__dict__['segments']=[]
            for segment in segments:
                sp = get_segment_stats(segment.id)
                if sp:
                    segment.__dict__['stats']=sp
                    segment.__dict__['quizzes']=[]
                    segment.__dict__['videos']=[]
                    segment.__dict__['lectures']=[]
                    modules = get_children(segment.id)
                    for mod in modules:
                        if mod.type=='quiz':
                            mp = get_quiz_stats(mod.id)
                            if mp:
                                mod.__dict__['stats']=mp
                                segment.__dict__['quizzes'].append(mod.__dict__)
                        elif mod.type=='video':
                            mp = get_video_stats(mod.id)
                            if mp:
                                mod.__dict__['stats']=mp
                                segment.__dict__['videos'].append(mod.__dict__)
                        elif mod.type=='lecture':
                            mp = get_lecture_stats(mod.id)
                            if mp:
                                mod.__dict__['stats']=mp
                                segment.__dict__['lectures'].append(mod.__dict__)
                    course.__dict__['segments'].append(segment.__dict__)
            res.append(course.__dict__)
    return res



