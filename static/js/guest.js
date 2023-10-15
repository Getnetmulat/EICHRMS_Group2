$(function() {
    // Masonry Grid
    $('.grid').isotope({
      filter: '*',
      // itemSelector: '.grid-item',
      masonry: {
        columnWidth: 180,
        fitWidth: true, // When enabled, you can center the container with CSS.
        gutter: 10
      }
      // layoutMode: 'fitRows'
    });
  
    $('.filter a').click(function(){
      $('.filter .current').removeClass('current');
      $(this).addClass('current');
  
      var selector = $(this).data('filter');
      $('.grid').isotope({
        filter: selector
      });
      return false;
    });
  
    // Fancybox
    $('.fancybox').fancybox({
      helpers: {
        overlay: { locked: false }
      }
    });
  });

  $('.search-input').focus(function(){
    $(this).parent().addClass('focus');
  }).blur(function(){
    $(this).parent().removeClass('focus');
  })
