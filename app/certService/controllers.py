import sys
import uuid
from .models import Certificate
from app import db
from config import Config

BASE_PATH = Config.BASE_PATH

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

def create_certificate_pending(courseId, userId, courseName, userName, completed_at, scoredPoints, totalPoints):
    dt = completed_at.strftime("%m-%d-%Y")
    location = generate_cert(userName, courseName, dt)
    cert = Certificate(
            course_id       = courseId, 
            user_id         = userId, 
            scored_points   = scoredPoints, 
            total_points    = totalPoints,
            status          = 'READY',
            location        = location
    )
    db.session.add(cert)
    commit()
    return [courseId, userId]

def is_certificate_eligible(course, courseProgress):
        if courseProgress.completed_segments>=course.children:
                return True
        return False

def generate_cert(name, courseName, date):
    from PIL import ImageFont, ImageDraw, Image
    image = Image.open(BASE_PATH+'certs/template/certificate.jpg')
    draw = ImageDraw.Draw(image)
    widths = [610, 530, 140]
    heights = [40, 90, 16]

    startx = [210, 250, 700]
    starty = [450, 300, 590]
         
    txts = [courseName, name, date]
    size = [10,10,10]
    ttf  = [BASE_PATH+'fonts/'+n for n in ["Gabriola.ttf", "mighty.otf", "DejaVuSans.ttf"]]
    fonts = [ImageFont.truetype(ttf[i], size[i]) for i in range(3)]

    for i in range(3):
        iw,ih = widths[i],heights[i]
        while True: 
            fw,fh = fonts[i].getsize(txts[i])
            if fw>iw or fh>ih:
                break
            size[i]+=1
            fonts[i] = ImageFont.truetype(ttf[i], size[i])
        alpha = 255
        r = 0 if i!=1 else 126
        g = 0 if i!=1 else 27
        b = 0 if i!=1 else 50
        dx = iw-fw if iw-fw>=0 else 0
        dy = ih-fh if ih-fh>=0 else 0
        sx = startx[i]+(dx//2)
        sy = starty[i]+(dy//2)
        draw.text((sx,sy), txts[i], font=fonts[i], fill=(r,g,b,alpha))
    loc = str(uuid.uuid4())+'.jpg'
    image.save(BASE_PATH+'certs/'+loc)
    return loc
