import urllib.request as request
import hashlib
import json
import base64
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
        'answer': ['plain', data['expected_answer']]}


def make_quiz(data):
    return {
        'input': ['quiz', data['input_data']],
        'answer': ['quiz', data['expected_answer']]}
