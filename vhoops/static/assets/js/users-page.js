$(function () {
  'use strict';

  var dt_basic_table = $('.datatables-basic'),
        dt_date_table = $('.dt-date'),
        ajax_config = $("#get-users");

  if (dt_basic_table.length) {
    var dt_basic = dt_basic_table.DataTable({
      ajax: ajax_config.attr('url'),
      columns: [
        { data: 'id' },
        { data: 'first_name' },
        { data: 'last_name' },
        { data: 'username' },
        { data: 'teams' },
        { data: 'groups' },
        { data: 'email' },
        { data: 'phone_number' },
        { data: 'registration_timestamp' }
      ],
      columnDefs: [
        {
          targets: 0,
          visible: false
        },
        {
          // Actions
          targets: 9,
          title: 'Actions',
          orderable: false,
          render: function (data, type, full, meta) {
            return (
              '<a href="javascript:;" class="delete-record" style="color: red;">' +
              feather.icons['trash-2'].toSvg({ class: 'mr-50 font-small-4' }) +
              '</a>'
            );
          }
        }
      ],
      order: [[1, 'desc']],
      dom:
        '<"card-header border-bottom p-1"<"head-label"><"dt-action-buttons text-right"B>><"d-flex justify-content-between align-items-center mx-0 row"<"col-sm-12 col-md-6"l><"col-sm-12 col-md-6"f>>t<"d-flex justify-content-between mx-0 row"<"col-sm-12 col-md-6"i><"col-sm-12 col-md-6"p>>',
      displayLength: 25,
      lengthMenu: [7, 10, 25, 50, 75, 100],
      buttons: [
        {
          extend: 'collection',
          className: 'btn btn-outline-secondary dropdown-toggle mr-2',
          text: feather.icons['share'].toSvg({ class: 'font-small-4 mr-50' }) + 'Export',
          buttons: [
            {
              extend: 'print',
              text: feather.icons['printer'].toSvg({ class: 'font-small-4 mr-50' }) + 'Print',
              className: 'dropdown-item'
            },
            {
              extend: 'csv',
              text: feather.icons['file-text'].toSvg({ class: 'font-small-4 mr-50' }) + 'Csv',
              className: 'dropdown-item'
            },
            {
              extend: 'excel',
              text: feather.icons['file'].toSvg({ class: 'font-small-4 mr-50' }) + 'Excel',
              className: 'dropdown-item'
            },
            {
              extend: 'pdf',
              text: feather.icons['clipboard'].toSvg({ class: 'font-small-4 mr-50' }) + 'Pdf',
              className: 'dropdown-item'
            },
            {
              extend: 'copy',
              text: feather.icons['copy'].toSvg({ class: 'font-small-4 mr-50' }) + 'Copy',
              className: 'dropdown-item'
            }
          ],
          init: function (api, node, config) {
            $(node).removeClass('btn-secondary');
            $(node).parent().removeClass('btn-group');
            setTimeout(function () {
              $(node).closest('.dt-buttons').removeClass('btn-group').addClass('d-inline-flex');
            }, 50);
          }
        },
        {
          text: feather.icons['plus'].toSvg({ class: 'mr-50 font-small-4' }) + 'Add New User',
          className: 'create-new btn btn-primary',
          attr: {
            'data-toggle': 'modal',
            'data-target': '#modals-slide-in'
          },
          init: function (api, node, config) {
            $(node).removeClass('btn-secondary');
          }
        }
      ],
      responsive: {
        details: {
          display: $.fn.dataTable.Responsive.display.modal({
            header: function (row) {
              var data = row.data();
              return 'Details of ' + data['full_name'];
            }
          }),
          type: 'column',
          renderer: function (api, rowIdx, columns) {
            var data = $.map(columns, function (col, i) {
              console.log(columns);
              return col.title !== '' // ? Do not show row in modal popup if title is blank (for check box)
                ? '<tr data-dt-row="' +
                    col.rowIndex +
                    '" data-dt-column="' +
                    col.columnIndex +
                    '">' +
                    '<td>' +
                    col.title +
                    ':' +
                    '</td> ' +
                    '<td>' +
                    col.data +
                    '</td>' +
                    '</tr>'
                : '';
            }).join('');

            return data ? $('<table class="table"/>').append(data) : false;
          }
        }
      },
      language: {
        paginate: {
          // remove previous & next text from pagination
          previous: '&nbsp;',
          next: '&nbsp;'
        }
      }
    });
//    $('div.head-label').html('<h6 class="mb-0">DataTable with Buttons</h6>');
  }

  // Flat Date picker
  if (dt_date_table.length) {
    dt_date_table.flatpickr({
      monthSelectorType: 'static',
      dateFormat: 'm/d/Y'
    });
  }

  // Delete Record
  $('.datatables-basic tbody').on('click', '.delete-record', function () {
    var tr = dt_basic.row($(this).parents('tr'));
    var data = tr.data();
    var ajax_config = $("#delete-user");
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
            url: ajax_config.attr("url").replace(0, data.id),
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

  var phoneMask = $('.phone-number');

  if (phoneMask.length) {
    new Cleave(phoneMask, {
      phone: true,
      phoneRegionCode: 'TR'
    });
  }

  var teamSelect = $('.team-name');
  teamSelect.wrap('<div class="position-relative"></div>').select2({
    dropdownAutoWidth: true,
    width: '100%',
    maximumSelectionLength: 2,
    dropdownParent: teamSelect.parent(),
    placeholder: 'Select maximum 2 items'
  });

  var groupSelect = $('.group-name');
  groupSelect.wrap('<div class="position-relative"></div>').select2({
    dropdownAutoWidth: true,
    width: '100%',
    dropdownParent: groupSelect.parent()
  });

});
