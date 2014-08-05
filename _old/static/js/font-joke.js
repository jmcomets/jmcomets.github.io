'use strict';

(function($) {
  $(window).load(function() {
    $('#font-joke').one('click', function() {
      $('head').append('<style>*{ font-family: "Comic Sans Ms" !important; }</style>');
      $(this).text('Sucka').append('&nbsp; <i class="fe fe-emo-devil"></i>');
      return false;
    });
  });
}) (jQuery);
