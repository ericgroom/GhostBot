import json


def json_browser(data: dict):
    json_str = json.dumps(data)
    filename = 'tmp.json'
    with open(filename, 'w') as f:
        f.write(json_str)
