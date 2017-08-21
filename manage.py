import os
from app import create_app, db
from flask_migrate import Migrate
from app.reportingService.models import *

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
migrate = Migrate(app, db)
