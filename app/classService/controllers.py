import sys

from .models import Module, CourseData
from app import db
from sqlalchemy.exc import SQLAlchemyError

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

def _get_module(id):
    m = Module.query.get(id)
    return m

def _get_parent_id(id):
    m = Module.query.with_entries(Module.parent).filter(Module.id == id).scalar()
    return m

def _get_modules_by_parent(parentId):
    children = Module.query.filter_by(parent=parentId).order_by(Module.serial)
    return children

def _get_module_count_by_parent(parentId):
    count = Module.query.filter_by(parent=parentId).count()
    return count

def create_module(type, name, serial, parent, author=None, children=0, location=None, expires_in=None, is_ready=False):
    module = Module(type=type, name=name, serial=serial, parent=parent, author=author, children=children, location=location, is_ready=is_ready)
    db.session.add(module)
    commit()
    return module.id

def _update_module_add_children(id):
    module = _get_module(id)
    module.children+=1

def _update_module_drop_children(id):
    module = _get_module(id)
    module.children-=1

def _update_module_change_location(id, location):
    module = _get_module(id)
    module.location = location

def _update_module(id, name, author, location, expires=None, is_ready=False):
    module = _get_module(id)
    if not module:
        #TODO: log
        raise SQLAlchemyError('Unable to find module')
    if module.name!=name:
        module.name=name
    if module.author!=author:
        module.author=author
    if module.location!=location:
        module.location=location
    if module.expires_in!=expires:
        module.expires_in=expires
    if module.is_ready!=is_ready:
        module.is_ready=is_ready
    return module.id

def _update_module_order(parentId, modules):
    existingModules = _get_modules_by_parent(parentId).all()
    modulesById = {}
    for mod in existingModules:
        modulesById[mod.id]=mod
    for i,moduleId in enumerate(modules):
        module = modulesById[moduleId]
        if module.serial!=i+1:
            module.serial=i+1
    return

def _delete_module(mod):
    parentId = mod.parent
    nextSiblings = _get_modules_by_parent(parentId).filter_by(Module.serial>mod.serial).all()
    db.session.delete(mod)
    for siblings in nextSiblings:
        siblings.serial-=1
    return

def _delete_modules_by_parent(parentId):
    modules = _get_modules_by_parent(parentId)
    modules.delete()

'''
entry methods to get, create, update [course, segment, quiz, video, lecture]
'''
def get_module(id):
    return _get_module(id)

def get_course_data(id):
    cd = CourseData.query.get(id)
    return cd

def get_parent_id(id):
    return _get_parent_id(id)

def get_children(parentId):
    mods = _get_modules_by_parent(parentId)
    return mods.all()

def get_child_by_serial(parentId, serial):
    if not parentId or serial<1:
        return None
    children = get_children(parentId)
    if serial>len(children):
        return None
    return children[serial-1]

def get_total_children(id):
    children = Module.query.with_entities(Module.children).filter(Module.id == id).scalar()
    return children

def get_expiry_by_id(id):
    expiry = Module.query.with_entities(Module.expires_in).filter(Module.id == id).scalar()
    return expiry

'''
course methods (Create,Edit,Update)
'''
def get_courses():
    courses = _get_modules_by_parent(None)
    m = courses.all()
    return m

def get_course_count():
    count = _get_module_count_by_parent(None)
    return count

def create_course(name, author, expires=None, serial=None, is_ready=False):
    if not serial:
        serial = get_course_count()+1
    courseid = create_module('course', name, serial, None, author, 0, None, expires, is_ready)
    return courseid

def update_course(id, name, author, expires=None, is_ready=False):
    courseId = _update_module(id, name, author, None, expires, is_ready)
    commit()
    return courseId

def update_course_order(newOrderListById):
    _update_module_order(None, newOrderListById)
    commit()
    return

def update_course_data(id, desc, duration, ppercent):
    cd = get_course_data(id)
    if cd:
        cd.description=desc
        cd.duration_weeks=duration
        cd.pass_percent=ppercent
        commit()
        return True
    return False

def create_course_data(id, desc, duration, pass_percent):
    cd = CourseData(id=id, description=desc, duration_weeks=duration, pass_percent=pass_percent)
    db.session.add(cd)
    commit()
'''
segment get, create, update
'''

def create_segment(name, courseId, author=None):
    serial = _get_module_count_by_parent(courseId)+1
    _update_module_add_children(courseId)
    segmentid = create_module('segment', name, serial, courseId, author)
    return segmentid

def update_segment(id, name, author):
    _update_module(id, name, author, None)
    commit()

def update_segment_order(courseId, newOrderListById):
    _update_module_order(courseId, newOrderListById)
    commit()

'''
quiz/lecture/video methods (CRUD)
'''

def create_quiz(name, segmentId, location, author=None):
    serial = _get_module_count_by_parent(segmentId)+1
    _update_module_add_children(segmentId)
    quizId = create_module('quiz', name, serial, segmentId, author, 0, location)
    return quizId

def create_video(name, segmentId, location, author=None):
    serial = _get_module_count_by_parent(segmentId)+1
    videoId = create_module('video', name, serial, segmentId, author, 0, location)
    return videoId

def create_lecture(name, segmentId, location, author=None):
    serial = _get_module_count_by_parent(segmentId)+1
    lectureId = create_module('lecture', name, serial, segmentId, author, 0, location)
    return lectureId

def update_lecture(id, name, location, author=None):
    lecture = _get_module(id)
    if not location:
        location = lecture.location
    _update_module(id, name, author, location)
    commit()
    return

def update_video(id, name, location, author=None):
    video = _get_module(id)
    if not location:
        location = video.location
    _update_module(id, name, author, location)
    commit()
    return

def update_quiz(id, name, location, author=None):
    quiz = _get_module(id)
    if not location:
        location = quiz.location
    _update_module(id, name, author, location)
    commit()
    return

'''
delete methods
'''

def delete_lecture(id):
    lecture = _get_module(id)
    _delete_module(lecture)
    commit()
    return

def delete_video(id):
    video = _get_module(id)
    _delete_module(video)
    commit()
    return

def delete_quiz(id):
    quiz = _get_module(id)
    parentId = quiz.parent
    _delete_module(quiz)
    _update_module_drop_children(parentId)
    commit()
    return

def delete_segment(id):
    segment = _get_module(id)
    _delete_modules_by_parent(id)
    courseId = segment.parent
    _delete_module(segment)
    _update_module_drop_children(courseId)
    commit()
    return

def delete_course(courseId):
    mod = _get_module(courseId)
    segments = _get_modules_by_parent(courseId).all()
    for segment in segments:
        _delete_modules_by_parent(segment.id)
        _delete_module(segment)
    _delete_module(mod)
    commit()
    return

def delete_course_data(courseId):
    cd = get_course_data(couseId)
    db.session.remove(cd)
    commit()

