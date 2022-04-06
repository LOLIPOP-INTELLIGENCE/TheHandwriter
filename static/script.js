
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
