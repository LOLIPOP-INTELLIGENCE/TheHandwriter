function nextClickScroll() {
    resSection = document.getElementById("choose-handwriting");
    resSection.scrollIntoView()

    // document.body.scrollTop = 10; // For Safari
    // document.documentElement.scrollTop = 10; // For Chrome, Firefox, IE and Opera
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

// function chooseFile ()
// {

//     var loc = document.getElementById ("hw-upload-form");

//     loc.appendChild (<p style="color: white; font-family: poppins;">Filename selected succesfully</p>);
// }

// Swiper Configuration
var swiper = new Swiper(".swiper-container", {
    slidesPerView: 1.5,
    spaceBetween: 10,
    centeredSlides: true,
    freeMode: true,
    grabCursor: true,
    loop: true,
    pagination: {
        el: ".swiper-pagination",
        clickable: true
    },
    autoplay: {
        delay: 4000,
        disableOnInteraction: false
    },
    navigation: {
        nextEl: ".swiper-button-next",
        prevEl: ".swiper-button-prev"
    },
    breakpoints: {
        500: {
            slidesPerView: 1
        },
        700: {
            slidesPerView: 1.5
        }
    }
});