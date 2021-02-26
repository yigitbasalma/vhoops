var teamSelect = $('.team-name');
teamSelect.wrap('<div class="position-relative"></div>').select2({
    dropdownAutoWidth: true,
    width: '100%',
    maximumSelectionLength: 2,
    dropdownParent: teamSelect.parent(),
    placeholder: 'Select maximum 2 items'
});

var conditionNotSelect = $('.condition-not-name');
conditionNotSelect.wrap('<div class="position-relative"></div>').select2({
    dropdownAutoWidth: true,
    width: '100%',
    maximumSelectionLength: 2,
    dropdownParent: conditionNotSelect.parent(),
    placeholder: 'Select maximum 2 items'
});

var conditionSelect = $('.condition-name');
conditionSelect.wrap('<div class="position-relative"></div>').select2({
    dropdownAutoWidth: true,
    width: '100%',
    maximumSelectionLength: 2,
    dropdownParent: conditionSelect.parent(),
    placeholder: 'Select maximum 2 items'
});

var columnSelect = $('.column-name');
columnSelect.wrap('<div class="position-relative"></div>').select2({
    dropdownAutoWidth: true,
    width: '100%',
    maximumSelectionLength: 2,
    dropdownParent: columnSelect.parent(),
    placeholder: 'Select maximum 2 items'
});

var integrationSelect = $('.integration-name');
integrationSelect.wrap('<div class="position-relative"></div>').select2({
    dropdownAutoWidth: true,
    width: '100%',
    maximumSelectionLength: 2,
    dropdownParent: integrationSelect.parent(),
    placeholder: 'Select maximum 2 items'
});

var responsibleSelect = $('.responsible-name');
responsibleSelect.wrap('<div class="position-relative"></div>').select2({
    dropdownAutoWidth: true,
    width: '100%',
    maximumSelectionLength: 2,
    dropdownParent: responsibleSelect.parent(),
    placeholder: 'Select maximum 2 items'
});

$('.datatables-basic tbody').on('click', '.delete-rule', function () {
    var tr = $(this).parents('tr');
    var rule_id = tr[0].cells[0].innerText;
    var ajax_config = $("#delete-rule");
    Swal.fire({
      title: 'Are you sure?',
      text: "You won't be able to revert this!",
      icon: 'warning',
      showCancelButton: true,
      confirmButtonColor: '#3085d6',
      cancelButtonColor: '#d33',
      confirmButtonText: 'Yes, delete it!'
    }).then((result) => {
      if (result.isConfirmed) {
        $.ajax({
            type: ajax_config.attr("method"),
            url: ajax_config.attr("url").replace(0, rule_id),
            success: function (data) {
                Swal.fire({
                  icon: data.status,
                  title: data.message,
                  showConfirmButton: false,
                  timer: 2000
                })

                if (data.status == "success") {
                  tr.remove().draw();
                }
            }
        });
      }
    })
});

$('.datatables-basic tbody').on('click', '.delete-notification-rule', function () {
    var tr = $(this).parents('tr');
    var rule_id = tr[0].cells[0].innerText;
    var ajax_config = $("#delete-notification-rule");
    Swal.fire({
      title: 'Are you sure?',
      text: "You won't be able to revert this!",
      icon: 'warning',
      showCancelButton: true,
      confirmButtonColor: '#3085d6',
      cancelButtonColor: '#d33',
      confirmButtonText: 'Yes, delete it!'
    }).then((result) => {
      if (result.isConfirmed) {
        $.ajax({
            type: ajax_config.attr("method"),
            url: ajax_config.attr("url").replace(0, rule_id),
            success: function (data) {
                Swal.fire({
                  icon: data.status,
                  title: data.message,
                  showConfirmButton: false,
                  timer: 2000
                })

                if (data.status == "success") {
                  tr.remove().draw();
                }
            }
        });
      }
    })
});