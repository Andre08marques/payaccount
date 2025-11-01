//pega o ano atual
$("#year").text(new Date().getFullYear());

// carousel
$('.carousel').carousel({
  interval: 6000,
  pause: 'hover'
});


 

// light box modal galeria fotos
$(document).on('click', '[data-toggle="lightbox"]', function (event) {
  event.preventDefault();
  $(this).ekkoLightbox();
});


//video play
$(function () {
  // Auto play
  $(".video").click(function () {
    var theModal = $(this).data("target"),
      videoSRC = $(this).attr("data-video"),
      videoSRCauto = videoSRC + "?modestbranding=1&rel=0&controls=0&showinfo=0&html5=1&autoplay=1";

    // Set the src of the iframe to the video URL with autoplay
    $(theModal + ' iframe').attr('src', videoSRCauto);

    // Optional: If you're using Bootstrap modals, use the 'hidden.bs.modal' event to reset the iframe src
    $(theModal).on('hidden.bs.modal', function () {
      $(theModal + ' iframe').attr('src', videoSRC);
    });
  });
});