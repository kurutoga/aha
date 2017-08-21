from app.classService.controllers import (
        get_module, get_parent_id, get_children,
        get_courses, get_child_by_serial,
        get_course_data
)
from app.studentService.controllers import (
        get_course_progress, get_quiz_progress, get_video_progress, 
        get_lecture_progress, get_or_create_segment_progress,
        create_course_progress, get_children_progress
)

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
        
