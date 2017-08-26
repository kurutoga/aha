import sys

from .models import Certificate
from app import db

'''
base methods
'''

def commit():
    try:
        db.session.commit()
    except:
        e = sys.exc_info()[0]
        #TODO: Log
        raise
    return

def get_certificate(courseId, userId):
    cert = Certificate.query.get([courseId, userId])
    return cert

def create_certificate_pending(courseId, userId, scoredPoints, totalPoints):
    cert = Certificate(
            course_id       = courseId, 
            user_id         = userId, 
            scored_points   = scoredPoints, 
            total_points    = totalPoints,
            status          = 'READY',
            location        = None
    )
    db.session.add(cert)
    commit()
    return [courseId, userId]

def is_certificate_eligible(course, courseProgress):
        if courseProgress.completed_segments>=course.children:
                return True
        return False

