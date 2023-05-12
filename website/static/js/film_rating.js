$(document).ready(function() {
    // Attach change event listener to all radio forms with class "rate"
    $('form.rate input[type=radio]').change(function() {
      // Retrieve selected radio button value and form ID
      var rating = $(this).val();
      var form_id = $(this).closest('form').attr('id');
      var film_id = form_id.split('_')[2];  // Extract film ID from form ID

      // Send AJAX POST request to Flask app
      $.ajax({
        type: 'POST',
        url: 'ajax/submit_rating',
        data: { 
            'rating': rating, 
            'film_id': film_id 
        },
        success: function(response) {
          console.log(response);  // Handle response (if needed)
        },
        error: function(error) {
          console.log(error);  // Handle error (if needed)
        }
      });
    });
  });
  