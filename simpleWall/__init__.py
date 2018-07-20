from flask import Flask
app = Flask(__name__)
from datetime import datetime



@app.template_filter('since')
def friendly_time(dt, past_="ago", 
    future_="from now", 
    default="just now"):
    """
    Returns string representing "time since"
    or "time until" e.g.
    3 days ago, 5 hours from now etc.
    """
    print("working with this dt", dt)
    now = datetime.now()
    print("working with this now", now)
    if now > dt:
        diff = now - dt
        dt_is_past = True
    else:
        diff = dt - now
        dt_is_past = False

    periods = (
        (diff.days / 365, "year", "years"),
        (diff.days / 30, "month", "months"),
        (diff.days / 7, "week", "weeks"),
        (diff.days, "day", "days"),
        (diff.seconds / 3600, "hour", "hours"),
        (diff.seconds / 60, "minute", "minutes"),
        (diff.seconds, "second", "seconds"),
    )
    print("periods", periods)

    for period, singular, plural in periods:
        print("here's what we got", period, singular, plural)
        
        if period >= 1:
            return "%d %s %s" % (period, \
                singular if period == 1 else plural, \
                past_ if dt_is_past else future_)

    return default