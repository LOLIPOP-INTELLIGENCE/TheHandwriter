import requests
from urllib.parse import unquote
import json

url = "https://dtpylwwmiaeer5nz6y2pkzrir40hymid.lambda-url.ap-south-1.on.aws/"

params = {
    "typed": "this is another random test stringthis is another random test stringthis is another random test stringthis is another random test stringthis is another random test stringthis is another random test stringthis is another random test stringthis is another random test stringthis is another random test stringthis is another random test stringthis is another random test stringthis is another random test stringthis is another random test stringthis is another random test stringthis is another random test stringthis is another random test stringthis is another random test stringthis is another random test stringthis is another random test stringthis is another random test stringthis is another random test stringthis is another random test stringthis is another random test stringthis is another random test string",
    "upl-hw": "https://i.imgur.com/r4EXvQY.jpg",
    "sel-hw": "3"
}

response = requests.get(url, params=params)
data = json.loads(response.text)
img_url_encoded = data['img_url']
img_url = unquote(img_url_encoded)

print(img_url)