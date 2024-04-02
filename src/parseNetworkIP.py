import json
import sys

# Read from stdin / pipe as a str
text = sys.stdin.read()

data = json.loads(text)

print(data["Networks"]["docker_csp-ce-net"]["IPAddress"])

