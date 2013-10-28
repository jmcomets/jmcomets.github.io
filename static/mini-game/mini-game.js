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
        'ganondorfSS': 'mini-game/spritesheets/ganondorf.png',
        'ganondorfSSdata': 'mini-game/spritesheets/ganondorf.json'
      });

      // Main stage
      var stage = new _.Stage(canvasId);

      // Ganondorf spritesheet
      var ganondorfSSdata = {
        framerate: 8,
        images: [resources['ganondorfSS']],
        animations: {
          walk: { frames: [5, 4, 3, 2, 1] },
          run: {
            frames: [5, 4, 3, 2, 1],
            speed: 2
          }
        }
      };
      $.ajax(resources['ganondorfSSdata'], {
        success: function(data) {
          ganondorfSSdata.frames = data.frames;
        }, async: false
      });
      var ganondorfSS = new _.SpriteSheet(ganondorfSSdata);

      // Ganondorf instance
      // TODO
      var ganondorf = new _.Sprite(ganondorfSS, 'walk');
      ganondorf.on('tick', function(evt) {
      });
      stage.addChild(ganondorf);

      // Game loop
      _.Ticker.timingMode = _.Ticker.RAF;
      _.Ticker.on('tick', function(evt) {
        stage.update(evt);
      });
    }) ('mini-game-canvas', createjs);

    // UI integration
    $('#mini-game-toggle').on('click', function() {
      var _ = createjs;
      _.Ticker.setPaused(!_.Ticker.getPaused());
      $('#mini-game-canvas').parents().first().slideToggle(500);
    });
  });
}) (jQuery);
