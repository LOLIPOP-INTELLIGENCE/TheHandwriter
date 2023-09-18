import base64
import requests

# Step 1: Read the image in binary mode
with open('/Users/blackhole/Desktop/VS_Code.nosync/TheHandwriter/static/scan.jpg', 'rb') as img_file:
    binary_data = img_file.read()

# Step 2: Encode the binary data to a base64 encoded string
upl_hw = base64.b64encode(binary_data).decode('utf-8')

# Step 3: Create the JSON payload
payload = {
    "queryStringParameters": {
        "typed": "running from docker with this script", 
        "upl-hw": "https://i.imgur.com/r4EXvQY.jpg", 
        "sel-hw": "3"
    }
}

# Step 4: Send the POST request
response = requests.post("http://localhost:9000/2015-03-31/functions/function/invocations", json=payload)

# Step 5: Print the response
print("Response:", response.text)
