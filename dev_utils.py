import json

def json_browser(dict):
    json_str = json.dumps(dict)
    filename = 'tmp.json'
    with open(filename, 'w') as f:
        f.write(json_str)
