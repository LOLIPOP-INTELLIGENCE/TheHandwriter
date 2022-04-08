
function nextClickScroll ()
{
    resSection = document.getElementById ("choose-handwriting");
    resSection.scrollIntoView ()

    // document.body.scrollTop = 10; // For Safari
    // document.documentElement.scrollTop = 10; // For Chrome, Firefox, IE and Opera
}

function userUploadHw ()
{
    resSection = document.getElementById ("user-upload-hw");
    resSection.scrollIntoView ();
}

function selectDefaultHw ()
{
    resSection = document.getElementById ("select-default-hw");
    resSection.scrollIntoView ();
}

function userUploadHwNext ()
{
    resSection = document.getElementById ("generate");
    resSection.scrollIntoView ();
}

function aboutUsClick ()
{
    resSection = document.getElementByClass("footer-");
    resSection.scroolIntoView ();
}

function ContactClick ()
{
    resSection = document.getElementByClass("contact");
    resSection.scroolIntoView ();
}

// function chooseFile ()
// {

//     var loc = document.getElementById ("hw-upload-form");

//     loc.appendChild (<p style="color: white; font-family: poppins;">Filename selected succesfully</p>);
// }