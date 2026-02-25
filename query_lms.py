import urllib.request
import json

data = json.dumps({
    "id": 1,
    "method": "slim.request",
    "params": ["-", ["pref", "cachedir", "?"]]
}).encode('utf-8')

req = urllib.request.Request('http://10.1.1.200:9000/jsonrpc.js', data=data, headers={'Content-Type': 'application/json'})
try:
    response = urllib.request.urlopen(req)
    result = json.loads(response.read().decode())
    print("LMS Response:", result)
except Exception as e:
    print(f"Error: {e}")
