'use strict';

(function($) {
  $(window).load(function() {
    $('#font-joke').one('click', function() {
      less.modifyVars({ '@base-font': 'Comic Sans Ms' });
      $(this).text('Sucka').append('&nbsp; <i class="fe fe-emo-devil"></i>');
    });
  });
}) (jQuery);
