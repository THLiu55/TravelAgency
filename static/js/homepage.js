$(function(){
    $('.carousel-item').eq(0).addClass('active1');
    var total = $('.carousel-item').length;
    var current = 0;
    $('#moveRight').on('click', function(){
      var next=current;
      current= current+1;
      setSlide(next, current);
    });
    $('#moveLeft').on('click', function(){
      var prev=current;
      current = current- 1;
      setSlide(prev, current);
    });
    function setSlide(prev, next){
      var slide= current;
      if(next>total-1){
       slide=0;
        current=0;
      }
      if(next<0){
        slide=total - 1;
        current=total - 1;
      }
             $('.carousel-item').eq(prev).removeClass('active1');
             $('.carousel-item').eq(slide).addClass('active1');
        setTimeout(function(){
  
        },800);
      
  
      
      console.log('current '+current);
      console.log('prev '+prev);
    }
  });

  // auto slide
  $(function(){
    var total = $('.carousel-item').length;
    var current = 0;
    setInterval(function(){
      var next=current;
      current= current+1;
      setSlide(next, current);
    }, 3000);
    function setSlide(prev, next){
      var slide= current;
      if(next>total-1){
       slide=0;
        current=0;
      }
      if(next<0){
        slide=total - 1;
        current=total - 1;
      }
             $('.carousel-item').eq(prev).removeClass('active1');
             $('.carousel-item').eq(slide).addClass('active1');
        setTimeout(function(){
  
        },800);
      
  
      
      console.log('current '+current);
      console.log('prev '+prev);
    }
  }
  );
  
  var messageBox = document.querySelector('.js-message');
  var btn = document.querySelector('.js-message-btn');
  var card = document.querySelector('.js-profile-card');
  var closeBtn = document.querySelectorAll('.js-message-close');

  btn.addEventListener('click',function (e) {
      e.preventDefault();
      card.classList.add('active');
  });

  closeBtn.forEach(function (element, index) {
     console.log(element);
      element.addEventListener('click',function (e) {
          e.preventDefault();
          card.classList.remove('active');
      });
  });

  // $(document).ready(function(){
  //   $(".containermenu").click(function () {
  //       $.ajax({
  //           url: '/category',
  //           type: 'post',
  //           data: {
  //               "category": $(this).attr('id')
  //           },
  //           success: function (data) {
  //               $(".cardcontainer").html(data);
  //               // $(".categorydiv").addClass("active");
  //           }
  //       })
  //   })
  //   })

// use ajax to change the content of the page
$(document).ready(function(){
  $(".clr").click(function () {
      $.ajax({
          url: '/category',
          type: 'post',
          data: {
              "category": $(this).attr('id')
          },
          success: function (data) {
              $(".cardcontainer").html(data);
              // $(".categorydiv").addClass("active");
          }
      })
  })
  })