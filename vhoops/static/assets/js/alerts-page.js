/*=========================================================================================
    File Name: app-email.js
    Description: Email Page js
    ----------------------------------------------------------------------------------------
    Item Name: Vuexy  - Vuejs, HTML & Laravel Admin Dashboard Template
    Author: PIXINVENT
    Author URL: http://www.themeforest.net/user/pixinvent
==========================================================================================*/

'use strict';

$(function () {
  var menuToggle = $('.menu-toggle'),
    sidebarToggle = $('.sidebar-toggle'),
    sidebarLeft = $('.sidebar-left'),
    sidebarMenuList = $('.sidebar-menu-list'),
    emailMediaList = $('.email-media-list'),
    emailAppList = $('.email-app-list'),
    emailUserList = $('.email-user-list'),
    emailUserListInput = $('.email-user-list .custom-checkbox'),
    emailScrollArea = $('.email-scroll-area'),
    listGroupMsg = $('.list-group-messages'),
    userActions = $('.user-action'),
    mailDelete = $('.mail-delete'),
    mailUnread = $('.mail-unread'),
    emailSearch = $('#email-search'),
    overlay = $('.body-content-overlay');

    // if it is not touch device
  if (!$.app.menu.is_touch_device()) {
    // Email left Sidebar
    if ($(sidebarMenuList).length > 0) {
      var sidebar_menu_list = new PerfectScrollbar(sidebarMenuList[0]);
    }

    // User list scroll
    if ($(emailUserList).length > 0) {
      var users_list = new PerfectScrollbar(emailUserList[0]);
    }

    // Email detail section
    if ($(emailScrollArea).length > 0) {
      var users_list = new PerfectScrollbar(emailScrollArea[0]);
    }
  }
  // if it is a touch device
  else {
    $(sidebarMenuList).css('overflow', 'scroll');
    $(emailUserList).css('overflow', 'scroll');
    $(emailScrollArea).css('overflow', 'scroll');
  }

    // Main menu toggle should hide app menu
  if (menuToggle.length) {
    menuToggle.on('click', function (e) {
      sidebarLeft.removeClass('show');
      overlay.removeClass('show');
    });
  }

  // Email sidebar toggle
  if (sidebarToggle.length) {
    sidebarToggle.on('click', function (e) {
      e.stopPropagation();
      sidebarLeft.toggleClass('show');
      overlay.addClass('show');
    });
  }

  // Overlay Click
  if (overlay.length) {
    overlay.on('click', function (e) {
      sidebarLeft.removeClass('show');
      overlay.removeClass('show');
    });
  }

  // Add class active on click of sidebar list
  if (listGroupMsg.find('a').length) {
    listGroupMsg.find('a').on('click', function () {
      if (listGroupMsg.find('a').hasClass('active')) {
        listGroupMsg.find('a').removeClass('active');
      }
      $(this).addClass('active');
      emailMediaList.find('li').remove();
      var filters = 'filters=status:' + $(this).attr('filter');
      getAlerts(filters);
    });
  }

  // For app sidebar on small screen
  if ($(window).width() > 768) {
    if (overlay.hasClass('show')) {
      overlay.removeClass('show');
    }
  }

  // Filter
  if (emailSearch.length) {
    emailSearch.on('keyup', function () {
      var value = $(this).val().toLowerCase();
      if (value !== '') {
        emailUserList.find('.email-media-list li').filter(function () {
          $(this).toggle($(this).text().toLowerCase().indexOf(value) > -1);
        });
        var tbl_row = emailUserList.find('.email-media-list li:visible').length;

        //Check if table has row or not
        if (tbl_row == 0) {
          emailUserList.find('.no-results').addClass('show');
          emailUserList.animate({ scrollTop: '0' }, 500);
        } else {
          if (emailUserList.find('.no-results').hasClass('show')) {
            emailUserList.find('.no-results').removeClass('show');
          }
        }
      } else {
        // If filter box is empty
        emailUserList.find('.email-media-list li').show();
        if (emailUserList.find('.no-results').hasClass('show')) {
          emailUserList.find('.no-results').removeClass('show');
        }
      }
    });
  }

  function serializeTags(tags) {
    var serialized = "";
    $.each(tags.split(","), function( index, value ) {
        serialized += '<span class="mr-50 badge badge-light-secondary">'+ value +'</span>'
    });
    return serialized;
  }

  function isSeen(seen) {
    if (seen == 1) {
        return 'mail-read';
    }
    return '';
  }

  function isSnoozed(snoozed) {
    if (snoozed == 1) {
        return '<span class="mr-50 badge badge-light-success" data-toggle="tooltip" data-placement="top" title="Alert acknowledged"><i data-feather="eye-off"></i></span>';
    }
    return '';
  }

  function snoozedUntil(s_date) {
    if (s_date != 'None') {
       return '<span class="mr-50 badge badge-light-success" data-toggle="tooltip" data-placement="top" title="Acknowledged until">'+ s_date +'</span>';
    }
    return '';
  }

  function lastOccurredAt(l_date) {
    if (l_date) {
        return '<span class="mr-50 badge badge-light-warning" data-toggle="tooltip" data-placement="top" title="Last occurred time.(Count must be more than 1)">'+ l_date +'</span>';
    }
    return '';
  }

  function getAlerts(filters) {
    var ajax_config = $("#get-alerts");

    if ( ! filters ) {
        var filters = 'filters=status:all';
    }

    $.ajax({
        type: ajax_config.attr('method'),
        url: ajax_config.attr('url') + '?' + filters,
        success: function (data) {
            if (data.data.length > 0) {
                if (emailUserList.find('.no-results').hasClass('show')) {
                    emailUserList.find('.no-results').removeClass('show');
                }

                $.each(data.data, function( index, value ) {
                    emailMediaList.append('<li class="media '+ isSeen(value['is_seen']) +'" id="alert-'+ value['id'] +'">' +
                        '<div class="media-body">' +
                            '<div class="mail-details">' +
                                '<div class="mail-items">' +
                                    '<h5 class="mb-25">'+ value['alias'] +'</h5>' +
                                    '<span class="text-truncate"> '+ serializeTags(value['tags']) +' </span>' +
                                '</div>' +
                                '<div class="mail-meta-item">' +
                                    '<span class="mr-50 badge badge-light-secondary" data-toggle="tooltip" data-placement="top" title="Alert status.">'+ value['status'] +'</span>' +
                                    '<span class="mr-50 badge badge-light-secondary" data-toggle="tooltip" data-placement="top" title="Alert count. (Calculating by alias)">#'+ value['alert_count'] +'</span>' +
                                    '<span class="mr-50 badge badge-light-secondary" data-toggle="tooltip" data-placement="top" title="Alert source.">'+ value['source'] +'</span>' +
                                    '<span class="mr-50 badge badge-light-secondary" data-toggle="tooltip" data-placement="top" title="Team name for alert.">'+ value['team']['name'] +'</span>' +
                                    '<span class="mr-50 badge badge-light-danger" data-toggle="tooltip" data-placement="top" title="Alert priority.">'+ value['priority'] +'</span>' +
                                    '<span class="mr-50 badge badge-light-info" data-toggle="tooltip" data-placement="top" title="Occurred at time.">'+ value['registration_timestamp'] +'</span>' +
                                    lastOccurredAt(value['lsat_occurred_at']) +
                                    isSnoozed(value['snoozed']) +
                                    snoozedUntil(value['snoozed_until']) +
                                '</div>' +
                            '</div>' +
                            '<div class="mail-message">' +
                                '<p class="text-truncate mb-0">'+ value['message'] +'</p>' +
                            '</div>' +
                        '</div>' +
                    '</li>')
                });

                if (feather) {
                    feather.replace({
                        width: 14,
                        height: 14
                    });
                }

                emailUserList.find('li').on('click', function (e) {
                      var details_page_ajax_config = $("#alert-details");
                      window.location.href = details_page_ajax_config.attr('url').replace(0, this.id.split('-')[1]);
                });
            } else {
                emailUserList.find('.no-results').addClass('show');
                emailUserList.animate({ scrollTop: '0' }, 500);
            }
        }
    });
  }

  getAlerts();

  var urlParams = new URLSearchParams(window.location.search);
  if (urlParams.has('error')) {
    toastr['error'](urlParams.get('error'), 'Not Completed!', {
      closeButton: true,
      tapToDismiss: false
    });
  }

});

$(window).on('resize', function () {
  var sidebarLeft = $('.sidebar-left');
  // remove show classes from sidebar and overlay if size is > 992
  if ($(window).width() > 768) {
    if ($('.app-content .body-content-overlay').hasClass('show')) {
      sidebarLeft.removeClass('show');
      $('.app-content .body-content-overlay').removeClass('show');
    }
  }
});
