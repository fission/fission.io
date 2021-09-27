//document.getElementsByClassName('menu-container').style.width = window.innerWidth - 80 + 'px';

window.onscroll = function () {
    scrollFunction();
};

function scrollFunction() {
    if (document.body.scrollTop > 50 || document.documentElement.scrollTop > 50) {
        document.getElementsByClassName('header')[0].style.background = "url('/images/hero-bg.png') no-repeat center fixed";
    } else {
        document.getElementsByClassName('header')[0].style.background = "transparent";
    }
}
