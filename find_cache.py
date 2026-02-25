import urllib.request
import json

data = json.dumps({
    "id": 1,
    "method": "slim.request",
    "params": ["-", ["serverstatus", 0, 99]]
}).encode('utf-8')

req = urllib.request.Request('http://localhost:9000/jsonrpc.js', data=data, headers={'Content-Type': 'application/json'})
try:
    response = urllib.request.urlopen(req)
    result = json.loads(response.read().decode())
    # The serverstatus doesn't directly return cachedir, let's just ask for server prefs
    print("Server connected successfully.")
except Exception as e:
    print(f"Error: {e}")

# To get the cachedir, we can just look at the default location for LMS on Windows
import os
default_paths = [
    r"C:\ProgramData\Lyrion\Cache",
    r"C:\ProgramData\Squeezebox\Cache",
    r"C:\Users\Igland\AppData\Roaming\Lyrion\Cache",
    r"C:\Users\Igland\AppData\Local\Lyrion\Cache",
]

for p in default_paths:
    if os.path.exists(p):
        print("Found Cache:", p)
