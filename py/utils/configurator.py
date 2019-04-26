import json
import os


def configure(app):
    path = os.path.realpath(
        os.path.join(os.getcwd(), os.path.dirname(__file__)))
    config_from_file(app, path + '/../config.json')
    additional_cfg = path + '/../../.config-custom.json'
    if os.path.isfile(additional_cfg):
        config_from_file(app, additional_cfg)


def config_from_file(app, filename):
    with open(filename) as cfg_json:
        cfg = json.load(cfg_json)
        for key in cfg:
            val = cfg[key]
            if isinstance(val, str) and val[0] == '$':
                app.config[key] = os.environ.get(val[1:])
            else:
                app.config[key] = val
