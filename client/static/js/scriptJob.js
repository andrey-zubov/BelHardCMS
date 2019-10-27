$('document').ready(function () {
    $('select#id_cv option').each(function () {
              $(this).remove()
    })

  $('#id_client').on('change', function () {
      var id = $(this).val();
      $.ajax({'url':'/client/admin_jobinterviews/',
      'data':{'id_client':id},
      success:function (data) {
          data = JSON.parse(data)

          $('select#id_cv option').each(function () {
              $(this).remove()
          })

          $.each(data, function (key, value) {
            $("select#id_cv").append('<option value=' + key + '>' + value + '</option>');
        });

      }})
    })
})