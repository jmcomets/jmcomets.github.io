(function($) {
  // Mini-game setup
  var canvas = $('#mini-game-canvas');

  // UI event for hiding/showing the mini-game
  $(window).load(function() {
    $('#mini-game-toggle').on('click', function() {
      $('#mini-game-canvas').parents().first().slideToggle(500);
    });
  });
}) (jQuery);
