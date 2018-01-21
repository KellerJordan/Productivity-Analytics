from actions import BlockPage, GetLinks, BlockLinks, MessageType
import requests
import json

def run(data):
    if data['type'] == MessageType.UrlGoto:
        return GetLinks(data['id'])
    elif data['type'] == MessageType.LinkDump:
        json_data = json.dumps({'urls': data['links']})
        r = requests.post('http://ec2-54-215-220-149.us-west-1.compute.amazonaws.com:8080/predict', json=json_data)
        if r.status_code != 200:
            return None

        rJson = r.json()

        return BlockLinks(data['id'], rJson)
