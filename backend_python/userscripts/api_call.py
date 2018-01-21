import requests
import json

def run(data):
	json_data = json.dumps(data)
	r = requests.post('http://ec2-54-215-220-149.us-west-1.compute.amazonaws.com:8080/predict', json=json_data)
	print r.text