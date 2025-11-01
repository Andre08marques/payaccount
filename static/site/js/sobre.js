//pega o ano atual
$("#year").text(new Date().getFullYear());

 
// configurar o slider
$('.slider').slick({
    infinite: true,
    slideToShow: 1,
    slideToScroll: 1
});