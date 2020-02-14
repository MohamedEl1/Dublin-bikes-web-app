import requests
import json

url = "https://api.jcdecaux.com/vls/v1/stations?contract=dublin&apiKey=b0979801c4ff351dc53e4bf7120f76de43e10959"

response = requests.get(url)
data = response.text
parsed = json.loads(data)
print(json.dumps(parsed, indent=4))
