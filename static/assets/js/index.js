$('.like-btn').click(function() {

    var postid = $(this).data('postid');
  
    $.ajax({
      url: '/like/'+postid+'/', 
      method: 'GET',
  
      success: function(response) {
        //update like count
        $('.like-count').text(response.likeCount) 
      }
    });
  
  });