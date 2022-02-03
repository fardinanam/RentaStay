$(function () {
    'use strict';
    // Showing page loader
    $(window).on('load', function () {
        setTimeout(function () {
            $(".page_loader").fadeOut("fast");
        }, 200);
    });

    $('.hideMessage').on('click',function(){
        document.getElementById("message").style.display = "None";
    });

});

setTimeout(function(){
    $('#message').fadeOut('slow');
}, 4000)
