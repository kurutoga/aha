from app.classService.controllers import (
        get_module, get_parent_id, get_children,
        get_courses, get_child_by_serial,
        get_course_data, get_downloadables, get_downloadable
)
from app.studentService.controllers import (
        get_course_progress, get_quiz_progress, get_video_progress, 
        get_lecture_progress, get_or_create_segment_progress,
        create_course_progress, get_children_progress, get_segment_progress
)

def update_user_profile(id, name, nickname, sex, city, state, country, nationality, occupation):
    from app import db
    from app.authService.models import User
    user = User.query.get(id)
    user.name = name
    user.nickname = nickname
    user.sex = sex
    user.city = city
    user.state = state
    user.country = country
    user.nationality = nationality
    user.occupation = occupation
    db.session.commit()

def _get_downloadable(id):
    return get_downloadable(id)

def _get_downloadables():
    return get_downloadables()

def _get_course_data(id):
    return get_course_data(id)

def _get_module(id):
    return get_module(id)

def _get_status(id, userId):
    m = get_module(id)
    if m:
        if m.type=='quiz':
            return get_quiz_progress(m.id, userId)
        elif m.type=='video':
            return get_video_progress(m.id, userId)
        elif m.type=='lecture':
            return get_lecture_progress(m.id, userId)
        elif m.type=='segment':
            return get_or_create_segment_progress(m.id, m.parent, userId)
        elif m.type=='course':
            return get_course_progress(m.id, userId)
    return None

def _get_type(id):
    m = get_module(id)
    if m:
        return m.type
    return None

def _get_next_mod(id):
    m = get_module(id)
    if m:
        parent = m.parent
        child = get_child_by_serial(parent, m.serial+1)
        if not child:
            return get_module(parent)
        return child
    return None

def _get_prev_mod(id):
    m = get_module(id)
    if m:
        parent = m.parent
        return get_child_by_serial(parent, m.serial-1)

def _get_courses():
    return get_courses()

def _get_progress(userId):
    courses = get_courses()
    res = []
    for course in courses:
        cp = get_course_progress(course.id, userId)
        if cp:
            segments=get_children(course.id)
            course.__dict__['progress']=cp
            course.__dict__['segments']=[]
            for segment in segments:
                sp = get_segment_progress(segment.id, userId)
                if sp:
                    segment.__dict__['progress']=sp
                    segment.__dict__['quizzes']=[]
                    modules = get_children(segment.id)
                    for mod in modules:
                        if mod.type=='quiz':
                            mp = get_quiz_progress(mod.id, userId)
                            if mp:
                                mod.__dict__['progress']=mp
                                segment.__dict__['quizzes'].append(mod.__dict__)
                    course.__dict__['segments'].append(segment.__dict__)
            res.append(course.__dict__)
    return res

def _get_courses_and_status(userId):
    courses = get_courses()
    progress = get_children_progress(courses, userId)
    available, inprogress, completed = [],[],[]
    for i,course in enumerate(courses):
        if course.is_ready:
            if progress[i]:
                course.__dict__['progress']=progress[i]
                if progress[i].is_complete:
                    completed.append(course)
                else:
                    inprogress.append(course)
            else:
                available.append(course)
    return available, inprogress, completed

def _get_segment_and_module_status(courseId, userId):
    segments = get_children(courseId)
    result   = []
    for segment in segments:
        d = segment.__dict__
        modules  = get_children(segment.id)
        progress = get_children_progress(modules, userId)
        d['modules'] = []
        for i, mod in enumerate(modules):
            dm = mod.__dict__
            if progress[i]:
                dm['progress']=progress[i]
            d['modules'].append(dm)
        result.append(d)
    return result
        
