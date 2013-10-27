"use strict";

(function($) {
  $(window).load(function() {
    // Mini-game
    (function(canvasId, _) {
      // Manifest: what to load
      var resources = (function(data) {
        for (var key in data) {
          data[key] = django.static(data[key]);
        }
        return data;
      }) ({
        'ganondorf': 'img/spritesheets/ganondorf.png'
      });

      // Main stage
      var stage = new _.Stage(canvasId);

      // Ganondorf
      var ganondorfSS = new _.SpriteSheet({
        framerate: 8,
        images: [resources['ganondorf']],
        frames: [
          [91, 63, 34, 64],
          [91, 925, 33, 59],
          [94, 864, 29, 59],
          [28, 952, 23, 60],
          [99, 2, 25, 59],
          [94, 803, 29, 59],
          [66, 411, 60, 49],
          [2, 321, 69, 50],
          [49, 803, 43, 72],
          [66, 517, 57, 53],
          [60, 626, 56, 53],
          [2, 692, 53, 59],
          [66, 462, 57, 53],
          [61, 572, 57, 52],
          [2, 583, 56, 53],
          [2, 638, 56, 52],
          [66, 517, 57, 53],
          [2, 110, 74, 55],
          [2, 167, 72, 52],
          [2, 426, 62, 50],
          [2, 373, 62, 51],
          [2, 221, 72, 50],
          [57, 742, 51, 59],
          [78, 129, 47, 74],
          [47, 877, 42, 73],
          [2, 2, 95, 53],
          [2, 57, 87, 51],
          [2, 753, 45, 75],
          [76, 272, 46, 76],
          [73, 350, 53, 59],
          [60, 681, 54, 59],
          [2, 830, 43, 61],
          [2, 529, 57, 52],
          [2, 478, 62, 49],
          [76, 205, 47, 65],
          [2, 273, 72, 46],
          [2, 952, 24, 60],
          [53, 952, 28, 59]
        ], animations: {
          walk: { frames: [5, 4, 3, 2, 1] },
          run: {
            frames: [5, 4, 3, 2, 1],
            speed: 2
          }
        }
      });

      var ganondorf = new _.Sprite(ganondorfSS, 'run');
      ganondorf.setTransform(0, 0, 1.5, 1.5);
      stage.addChild(ganondorf);

      _.Ticker.timingMode = _.Ticker.RAF;
      _.Ticker.addEventListener('tick', function(evt) {
        stage.update(evt);
      });
    }) ('mini-game-canvas', createjs);

    // UI integration
    $('#mini-game-toggle').on('click', function() {
      $('#mini-game-canvas').parents().first().slideToggle(500);
    });
  });
}) (jQuery);
