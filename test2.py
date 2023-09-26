import requests
import base64
import json
import boto3
import time

with open("test.jpg", "rb") as image_file:
    base64_image = base64.b64encode(image_file.read()).decode()

payload = {
        "upl_hw": base64_image,
}

print(base64_image[:100])


# URL of the Lambda function
url = "https://7z66tplb4pjpdvgd6lxyyhik7u0ndaah.lambda-url.ap-south-1.on.aws/"

# Make the POST request
response = requests.post(url, json=payload)
# Check for successful invocation
print((response))