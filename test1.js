const axios = require('axios');
const fs = require('fs');
const base64 = require('base-64');

// Read the image file and convert it to a Base64 string
fs.readFile('test.jpg', (err, data) => {
  if (err) {
    console.error('Error reading the file:', err);
    return;
  }
  const base64Image = Buffer.from(data).toString('base64');

  console.log(base64Image.slice(0, 100));

  const payload = {
    upl_hw: base64Image,
  };

  // URL of the Lambda function
  const url = 'https://7z66tplb4pjpdvgd6lxyyhik7u0ndaah.lambda-url.ap-south-1.on.aws/';

  fetch(url, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(payload),
  })
  .then(response => response.json())
  .then(data => {
    // Accessing specific keys from the response
    const path = data.path;
  
    console.log(`Path: ${path}`);
  })
  .catch((error) => {
    console.error('Error in POST request:', error);
  });
  
});
