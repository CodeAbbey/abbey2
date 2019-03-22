import _sys, json
from browser import document, window, alert
from javascript import JSConstructor

class Struct:
    def __init__(self):
        pass

def dict_to_obj(d):
    if type(d) is list:
        return list(map(dict_to_obj, d))
    if not type(d) is dict:
        return d
    o = Struct()
    for k in d:
        v = dict_to_obj(d[k])
        setattr(o, k, v)
    return o

def json_to_obj(s):
    return dict_to_obj(json.loads(s))

def done(operations):
    pass

def _input():
    return ''

def _write_err(x):
    alert(x)

def setup(write):
    _sys.stdout.write = write

def _time():
    Date = JSConstructor(window.Date)
    return Date().getTime()

def dbg(s):
    window.console.log(s)

def runner(just_check = True):
    ns = {'__name__':'__game__', 'setup':setup, 'done':done, '_time':_time,
        'input':_input, 'dbg':dbg}
    code = window.brEditor.getValue()
    try:
        lc = {}
        exec(code, ns, lc)
        if just_check:
            window.selfCheck(lc['count_win'])
        else:
            window.verifyAndSubmit(lc['count_win'])
    except Exception as e:
        dbg('exc: ' + str(e))
        window.modalAlert('Some Error:', str(e))

window.runner = runner

#_sys.stdout.write = _write
_sys.stderr.write = _write_err
