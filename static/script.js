
// stores what the user types in (this will later be used in the POST request while generating the handwriting)
var typed = "";

// stores which handwriting the user selects (if a default handwriting is selected)
var selected_hw = -1;

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

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

function generateClick () {

    // create a new post request which tells the server the typed text, selected handwriting
    // and requests it to create an image
    var xhr = new XMLHttpRequest();
    xhr.open("POST", "/res", true);

    // the browser sends a json object containing the typed text and selected handwriting, set
    // content-type header to application/json
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.setRequestHeader('X-CSRFToken', getCookie('csrftoken'));

    // set the body of the request and send it
    xhr.send(JSON.stringify({
        "typed": typed,
        "def-hw": selected_hw
    }));

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
