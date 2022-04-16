
// stores what the user types in (this will later be used in the POST request while generating the handwriting)
var typed           = "";

var upload_hw       = -1;

// stores which handwriting the user selects (if a default handwriting is selected)
var selected_hw     = -1;

// utility function to get session cookie (for post requests)
function getCookie(name) {
    var cookieValue     = null;
    if (document.cookie && document.cookie !== '') {
        var cookies     = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie  = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// utility function to convert from arrayBuffer to base 64 encoded bytes-string
function arrayBufferToBase64(buffer) {
    var binary = '';
    var bytes = [].slice.call(new Uint8Array(buffer));
    bytes.forEach((b) => binary += String.fromCharCode(b));
    return window.btoa(binary);
};

function restoreNextButton () {
    nextbutton = document.getElementById ("text-input-next");
    nextbutton.textContent = "Next";
}

function nextClickScroll() {

    textarea = document.getElementById ("textinput");
    typed = textarea.value;

    nextbutton = document.getElementById ("text-input-next");

    if (typed == "") {
        nextbutton.textContent = "Please enter some text first!";
        setTimeout (restoreNextButton, 3000);
    }
    else {
        resSection = document.getElementById("choose-handwriting");
        resSection.scrollIntoView()
    }
}

function userUploadHw() {
    resSection = document.getElementById("user-upload-hw");
    resSection.scrollIntoView();
}

function selectDefaultHw() {
    resSection = document.getElementById("select-default-hw");
    resSection.scrollIntoView();
}

function userUploadHwNext() {
    resSection = document.getElementById("generate");
    resSection.scrollIntoView();
}

function aboutUsClick() {
    resSection = document.getElementById("meet-the-team");
    resSection.scrollIntoView();
}

function contactClick() {
    resSection = document.getElementById("contact-us");
    resSection.scrollIntoView();
}

function defaultClick(number) {
    selected_hw = number
}

function uploadClick() {

    // var validExt = ["BMP", "GIF", "JPEG", "JPG", "LBM", "PCX", "PNG", "PNM", "SVG", "TGA", "TIFF", "WEBP", "XPM"];

    var uploadInput     = document.getElementById("upload-input");
    var uploadButton    = document.getElementById("upload-button");
    var numFiles        = uploadInput.files.length;

    // check to see if a file has been selected (the number of files selected should be non-zero)
    if (!(numFiles === 0)) {

        // get the file object and its name (complete path + extension)
        upload_hw       = uploadInput.files[0];
        var filename    = upload_hw.name;
        // var fileExt     = filename.split('.').pop().toUpperCase();

        // the text on the upload button should change if the image is valid
        // this does not change the behaviour of the button
        // clicking on the button will allow the user to select another file
        // selecting a new file (valid or not) will unselect the current file
        // if (validExt.indexOf(fileExt) != -1) {
        if (upload_hw.type.split('/')[0] === "image") {
            uploadButton.textContent = "\"" + filename + "\" selected";
        }
        else {

            // unselect the file
            upload_hw   = -1;

            // change the text (and color) to indicate invalid file (behaviour of button does not change)
            uploadButton.textContent = "File type not supported!";
            uploadButton.setAttribute("style", "width: 100% !important; color: #FF0000 !important;");

            // after 3 seconds, restore the text and color back to normal (once again, without altering behaviour)
            setTimeout(function () {
                var uploadButton = document.getElementById("upload-button");
                uploadButton.textContent = "Upload";
                uploadButton.setAttribute("style", "width: 100% !important;");
            }, 3000);
        }
    }
}

function goToResult () {

    // parse the returned string data int a json object, the object contains only one
    // member, the path, which is an extensionless string to the result image
    var data = JSON.parse(this.responseText);
    var path = data.path

    // open the result in a new tab
    window.open("http://localhost:8000/result/" + path, '_blank');

    // change the generate button to a redirect button
    var generateButtonExt  = document.getElementById("generate-button-extern");
    var generateButtonInt  = document.getElementById("generate-button-intern");

    // clicking should no longer send a post request, only redirect to the new page
    generateButtonExt.setAttribute("onclick", "");

    // the button should now open the result page in a new tab
    generateButtonInt.textContent = "Click here if not automatically redirected";
    generateButtonInt.setAttribute("href", "http://localhost:8000/result/" + path);
    generateButtonInt.setAttribute("target", "_blank");
}

async function generateClick () {

    // create a new post request which tells the server the typed text, selected handwriting
    // and requests it to create an image
    var xhr = new XMLHttpRequest();
    xhr.open("POST", "/res", true);

    // the browser sends a json object containing the typed text and selected handwriting, set
    // content-type header to application/json
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.setRequestHeader('X-CSRFToken', getCookie('csrftoken'));

    body = {"typed": typed, "def-hw": selected_hw, "upl-hw": -1};

    if (upload_hw != -1) {

        var txt = await upload_hw.arrayBuffer();
        txt = arrayBufferToBase64(txt);
        body["upl-hw"] = txt;
    }

    // set the body of the request and send it
    xhr.send(JSON.stringify(body));

    // on recieve a response, invoke the goToResult function which performs the redirection, etc.
    xhr.onload = goToResult;
}

// Swiper Configuration
var swiper = new Swiper(".swiper-container", {
    slidesPerView:          1.5,
    spaceBetween:           10,
    centeredSlides:         true,
    freeMode:               true,
    grabCursor:             true,
    loop:                   true,
    pagination: {
        el:                     ".swiper-pagination",
        clickable:              true
    },
    autoplay: {
        delay:                  4000,
        disableOnInteraction:   false
    },
    navigation: {
        nextEl:                 ".swiper-button-next",
        prevEl:                 ".swiper-button-prev"
    },
    breakpoints: {
        500: {
            slidesPerView:          1
        },
        700: {
            slidesPerView:          1.5
        }
    }
});
