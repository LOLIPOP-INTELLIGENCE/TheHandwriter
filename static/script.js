
//stores what the user types in (this will later be used in the POST request while generating the handwriting)
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

function generateClick () {

    var xhr = new XMLHttpRequest();

    xhr.open("POST", "/res", true);
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.setRequestHeader('X-CSRFToken', getCookie('csrftoken'));

    xhr.send(JSON.stringify({
        "typed": typed,
        "def-hw": selected_hw
    }));

    xhr.onload = function() {
        var data = JSON.parse(this.responseText);
        console.log(data);
    }

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
