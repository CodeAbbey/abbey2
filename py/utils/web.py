import functools
import flask


def login_required(f):
    @functools.wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in flask.session:
            return flask.redirect(
                flask.url_for('login_page', next=flask.request.url))
        return f(*args, **kwargs)
    return decorated_function


def no_cache(resp):
    if flask.request.endpoint not in ('static'):
        resp.headers.set(
            'Cache-Control',
            'no-store, no-cache, must-revalidate, post-check=0, pre-check=0')
        resp.headers.set('Expires', 'Fri, 20 Nov 1981 08:52:00 GMT')
        resp.headers.set('Pragma', 'no-cache')
    return resp
