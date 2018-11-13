import urllib.request as request
import hashlib
import json
import random
import time
import base64
import re
import flask


def checker_exec(checker_code):
    checker_code_s = checker_code.decode('utf-8')
    if checker_code_s.startswith('#php'):
        srv = flask.current_app.config['CHECKER_SERVER'].split(' ', 2)
        forhash = (srv[1] + checker_code_s.strip()).encode('utf-8')
        sha = hashlib.sha512(forhash).hexdigest()
        headers = {'X-HASH': sha}
        req = request.Request(srv[0], data=checker_code, headers=headers)
        with request.urlopen(req) as resp:
            data = resp.read()
        res = json.loads(data.decode('utf-8'))
        res['input_data'] = base64.b64decode(res['input_data']).decode('utf-8')
        res['expected_answer'] = \
            base64.b64decode(res['expected_answer']).decode('utf-8')
        return make_plain(res)
    else:
        local_vars = {}
        exec(checker_code, {}, local_vars)
        if 'check_type' not in local_vars:
            return make_plain(local_vars)
        elif local_vars['check_type'] == 'quiz':
            return make_quiz(local_vars)


def make_plain(data):
    return {
        'input': ['plain', data['input_data']],
        'answer': ['plain', data['expected_answer']],
        'timeout': time_limit(data)}


def make_quiz(data):
    input_data = data['input_data']
    qi = 0
    for q in input_data:
        ai = 0
        for a in q['items']:
            q['items'][ai] = {'id': 'qz%s%s' % (qi, ai), 'text': a}
            ai += 1
        qi += 1
        random.shuffle(q['items'])
    return {
        'input': ['quiz', input_data],
        'answer': ['quiz', data['expected_answer']],
        'timeout': time_limit(data)}


def time_limit(data):
    timeout = data.get('time_limit', [86400, '1 day'])
    timeout[0] += int(time.time())
    return timeout


def answer_from_form(check_type, form):
    if check_type == 'plain':
        return form.get('answer', None)
    elif check_type == 'quiz':
        return quiz_results(form)
    else:
        return None


def quiz_results(form):
    res = []
    r = re.compile(r'qz\d{2}')
    for key in form:
        if r.fullmatch(key):
            res.append(key[2:])
    res.sort()
    return ' '.join(res)


def quiz_wrong_percentage(expected, answer):
    expected = set(expected.split(' '))
    answer = set(answer.split(' '))
    missed = len(expected.difference(answer))
    extra = len(answer.difference(expected))
    return (missed + extra) * 50 / len(expected)
