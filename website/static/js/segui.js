
$(document).ready(function() {
    $('a.segui').on('click', function() {
      var btn_id = $(this).closest('a').attr('id');
      var id_amico = btn_id.split('_')[1];  
      console.log(id_amico);
      $.ajax({
        type: 'POST',
        url: '/ajax/segui',
        data: {id_amico: id_amico},
        success: function(response) {
          console.log(response);  
          location.reload();
        },
        error: function(error) {
          console.log(error);  
        }
      });
    });
  });
  