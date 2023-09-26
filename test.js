const url = "https://dtpylwwmiaeer5nz6y2pkzrir40hymid.lambda-url.ap-south-1.on.aws/";
// const params = {
//   "typed": "this is another random test string...",
//   "upl-hw": "-1",
//   "sel-hw": "3"
// };

const params = {
    "typed": "this is another random test string...",
    "upl-hw": "https://i.imgur.com/r4EXvQY.jpg",
    "sel-hw": "3"
  };

// Convert params object to a search string
const searchParams = new URLSearchParams(params);

// Make the GET request
fetch(`${url}?${searchParams.toString()}`)
  .then(response => response.json())
  .then(data => {
    const imgURLEncoded = data['img_url'];
    const imgURL = decodeURIComponent(imgURLEncoded);
    console.log(imgURL);
  })
  .catch(error => {
    console.error("Error:", error);
  });
