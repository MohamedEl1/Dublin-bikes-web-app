import requests
import json

# Connect to the URL
url = "https://api.jcdecaux.com/vls/v1/stations?contract=dublin&apiKey=b0979801c4ff351dc53e4bf7120f76de43e10959"

response = requests.get(url)

# Read the output
data = response.text

# converting the string to JSON
parsed = json.loads(data)

# “pretty print” to make it more readable
print(json.dumps(parsed, indent=4))
