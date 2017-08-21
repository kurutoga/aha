from app import cel
from .controllers import create_quiz_progress

@cel.task
def quiz_scoring_task(quizId, segmentId, courseId, userId, pp, ap, ppercent, apercent, tp, duration):
    create_quiz_progress(quizId, segmentId, courseId, userId, pp, ap, ppercent, apercent, tp, duration)

