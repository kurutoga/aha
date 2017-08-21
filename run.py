import os
from app import create_app
from app import cel
import app.studentService.tasks 

app = create_app(os.getenv('FLASK_CONFIG') or 'default')

if __name__=="__main__":
    app.run(host='0.0.0.0', port=3000, debug=True)
