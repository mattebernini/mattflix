$(document).ready(function() {
    $('form.rate input[type=radio]').change(function() {
      var rating = $(this).val();
      var form_id = $(this).closest('form').attr('id');
      var film_id = form_id.split('_')[2];  
      
      $.ajax({
        type: 'POST',
        url: '/ajax/submit_rating',
        data: { 
            'rating': rating, 
            'film_id': film_id 
        },
        success: function(response) {
          console.log(response);  
        },
        error: function(error) {
          console.log(error);  
        }
      });
    });
  });
  