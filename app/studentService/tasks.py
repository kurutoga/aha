from app import cel
from .controllers import create_quiz_progress, end_quiz

@cel.task
def quiz_scoring_task(quizId, segmentId, courseId, userId, userName, pp, ap, ppercent, apercent, tp, duration, raw_data=""):
    create_quiz_progress(quizId, segmentId, courseId, userId, userName, pp, ap, ppercent, apercent, tp, duration)
    end_quiz(quizId, userId, raw_data)
