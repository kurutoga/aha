from app import db

def _get_now():
    return datetime.datetime.now()

class ModuleProgress():
    moduleId = db.Column(db.Integer(), db.ForeignKey('module.id'), primary_key=True)
    userId = db.Column(db.Integer(), db.ForeignKey('user.id'), primary_key=True)
    created_at = db.Column(db.DateTime(), default=_get_now)
    modified_at = db.Column(db.DateTime(), onupdate=_get_now)
    data = db.Column(db.JSON)

class TopicProgress(db.Model, ModuleProgress):
    completedModules = db.Column(db.Integer())

class QuizProgress(db.Model, ModuleProgress):
    detailedXML = db.Column(db.Text)
    earnedPoints = db.Column(db.Float)
    passingScore = db.Column(db.Float)
    passingPercent = db.Column(db.Float)
    gainedScore = db.Column(db.Float)
    timeLimit = db.Column(db.Float)
    usedTime = db.Column(db.Float)

class VideoProgress(db.Model, ModuleProgress):
    duration = db.Column(db.Float)
    currentTime = db.Column(db.Float)
    completed = db.Column(db.Boolean)
    views = db.Column(db.Integer)

class LectureProgress(db.Model, ModuleProgress):
    totalSlides = db.Column(db.Integer)
    completedSlides = db.Column(db.Integer)

class ModuleStats():
    moduleId = db.Column(db.Integer(), db.ForeignKey('module.id'), primary_key=True)
    views = db.Column(db.Interger())
    created_at = db.Column(db.DateTime(), default=_get_now)
    modified_at = db.Column(db.DateTime(), onupdate=_get_now)

class QuizStats(ModuleStats, db.Model):
    attempts = db.Column(db.Integer, default=0)
    score = db.Column(db.Float, default=0.0)
    time = db.Column(db.Float, default=0.0)

class VideoStats(ModuleStats, db.Model):
    time = db.Column(db.Float, defauly=0.0)
    
