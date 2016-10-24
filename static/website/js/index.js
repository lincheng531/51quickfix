$(function () {
    var changeNav = function () {
        $('#nav-menu .nav-item .nav-link').removeClass('active');
        $('#nav-menu .nav-item .nav-link[href="'+window.location.pathname+'"]').addClass('active');;
    }
    changeNav();


    var posx = 0;
    window.setInterval(function () {
        if(posx > 99999999) {
            posx = 0;
        }
        $('#city-sketch').css('background-position-x', posx--);
    }, 100);
});