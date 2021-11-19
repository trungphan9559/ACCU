$(document).ready(function() {
  var el_sticky = $('.sticky').first();
  el_sticky.addClass('fixed');
});

$(function() {

  var lastId
  var  menuItems = $('#top-menu').find("a")
  var  topMenuHeight = $('#top-menu').outerHeight()+15
  var  scrollItems = menuItems.map(function(){
          var item = $($(this).attr("href"));
          if (item.length) { return item; }
        });
  
  $(document).on('click', 'a[href^="#"]', function (event) {
    event.preventDefault();
  
      $('.tab__anchorlink ul li').removeClass('active')
      $(this).parent().addClass('active')
    $('html, body').animate({
      scrollTop: $($.attr(this, 'href')).offset().top - 80
    }, 500);
  });
  
  
  
  $(window).scroll(function(){
      var sticky = $('.sticky'),
          scroll = $(window).scrollTop();
    
      if (scroll >= -1) sticky.addClass('fixed');
      else sticky.removeClass('fixed');
  
      var fromTop = $(this).scrollTop() + 120;
      var cur = scrollItems.map(function(){
        if ($(this).offset().top < fromTop)
          return this;
      });
      cur = cur[cur.length-1];
      var id = cur && cur.length ? cur[0].id : "";
      
      if (lastId !== id) {
          lastId = id;
          // Set/remove active class
          menuItems
            .parent().removeClass("active")
            .end().filter("[href='#"+id+"']").parent().addClass("active");
      }   
    });
  
   var offsetWindow = $(document).scrollTop();
    if(offsetWindow > 100) {
      $('.sticky').addClass('fixed')
    } 
  });
  
  