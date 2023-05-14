$(document).ready(function() {
    $('form.da_vedere input[type=checkbox]').change(function() {
      
    var da_vedereValue = $(this).is(':checked');
    var form_id = $(this).closest('form').attr('id');
    var film_id = form_id.split('_')[2];  
    console.log(film_id);

      $.ajax({
        type: 'POST',
        url: '/ajax/submit_da_vedere',
        data: { 
            'da_vedere': da_vedereValue, 
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
  