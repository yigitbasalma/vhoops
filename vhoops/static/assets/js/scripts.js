(function (window, undefined) {
  'use strict';

  $('form').on('submit', function (e) {
    e.preventDefault();
    var form = $(this);
    var form_data = form.serialize();
    $.ajax({
        type: form[0].method,
        url: form[0].action,
        data: form_data,
        success: function (data) {
            if (data.message) {
                if (data.redirect) {
                    window.location.replace(data.redirect);
                } else {
                    Swal.fire({
                      icon: data.status,
                      title: data.message,
                      showConfirmButton: false,
                      timer: 2000
                    })

                    setTimeout(function(){
                        if (data.refresh) {
                            location.reload(true);
                        }
                    }, 2000);
                }
            }
        }
    });
  });

})(window);
