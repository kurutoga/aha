from functools import wraps, update_wrapper
from datetime import datetime, date, timedelta
import uuid
from werkzeug.http import http_date
from flask import make_response, request, url_for

def _get_now():
    return datetime.now()

def add_years(d, years=1):
    """Return a date that's `years` years after the date (or datetime)
    object `d`. Return the same calendar date (month and day) in the
    destination year, if it exists, otherwise use the following day
    (thus changing February 29 to March 1).

    """
    try:
        return d.replace(year = d.year + years)
    except ValueError:
        return d + (date(d.year + years, 1, 1) - date(d.year, 1, 1))

def add_days(d, days):
    return d + timedelta(days=days)

def redirect_url(default='core.home'):
    return request.args.get('next') or \
           request.referrer or \
           url_for(default)

def nocache(view):
    @wraps(view)
    def no_cache(*args, **kwargs):
        response = make_response(view(*args, **kwargs))
        response.headers['Last-Modified'] = http_date(datetime.now())
        response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0'
        response.headers['Pragma'] = 'no-cache'
        return response
        
    return update_wrapper(no_cache, view)

def convert_to_uuid(s):
    return uuid.UUID(s)
