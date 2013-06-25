"""
Use the functions in this module to supplement the datetime module in the
standard library.

author:  Isaac Johnston
date  :  June 19, 2013

"""
import calendar
from datetime import datetime, timedelta

def utc_to_local(utc_dt):
    """
    Convert a utc datetime object to a local datetime object.

    """
    timestamp = calendar.timegm(utc_dt.timetuple())
    local_dt = datetime.fromtimestamp(timestamp)
    assert utc_dt.resolution >= timedelta(microseconds=1)
    return local_dt.replace(microsecond=utc_dt.microsecond)
