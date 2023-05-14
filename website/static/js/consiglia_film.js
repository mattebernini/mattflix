$(document).ready(function() {
    $('form.consiglia_film input[type=checkbox]').change(function() {
      
    var consigliaValue = $(this).is(':checked');
    var form_id = $(this).closest('form').attr('id');
    var film_id = form_id.split('_')[2];  
    console.log(film_id);

      $.ajax({
        type: 'POST',
        url: '/ajax/submit_consiglia',
        data: { 
            'consiglia': consigliaValue, 
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
  