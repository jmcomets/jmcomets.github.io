"use strict";

(function($) {
  $(window).load(function() {
    // Mini-game
    (function(canvasId, _) {
      // Spritesheet data/images to load
      var spriteSheets = (function(targets) {
        var data = {};

        for (var i = 0; i < targets.length; i++) {
          var target = targets[i],
            base = staticURI('mini-game/spritesheets/' + target);
          data[target] = {};
          data[target].image = base + '.png';
          data[target].data = base + '.json';
        }

        return data;
      }) (['ganondorf-left', 'ganondorf-right']);

      // Keyboard event dispatcher (use to bind key events)
      var keyboard = new _.EventDispatcher();

      // Main stage
      var stage = new _.Stage(canvasId);
      //...helpers
      stage.height = stage.canvas.height;
      stage.width = stage.canvas.width;
      //...center origin for stage
      stage.regX = -stage.width/2;
      stage.regY = -stage.height/2;

      // Ganondorf spritesheets
      var ganondorfSS = (function(data) {
        var res = [], ss = ['left', 'right'];

        for (var i = 0; i < ss.length; i++) {
          var spriteSheet = spriteSheets['ganondorf-' + ss[i]];

          // Images to load for spritesheet
          data.images = [spriteSheet.image];

          // Load spritesheet JSON data
          $.ajax({
            url: spriteSheet.data,
            success: function(jsonData) {
              data.frames = jsonData.frames;
            }, async: false
          });

          res[ss[i]] = new _.SpriteSheet(data);
        }

        return res;
      }) ({
        framerate: 8,
        animations: {
          idle: {
            frames: [2]
          }, walk: {
            frames: [5, 4, 3, 2, 1]
          }, run: {
            frames: [5, 4, 3, 2, 1],
            speed: 2
          }
        }
      });

      // Ganondorf sprite
      var ganondorf = new _.Sprite(ganondorfSS['left'], 'idle');
      stage.addChild(ganondorf);

      // Ganondorf logic
      var ganondorfLogic = {
        state: {
          direction: 'left',
          motion: 0,
          speed: 3
        }, move: function(direction) {
          assert(direction == 'left' || direction == 'right');
          this.state.direction = direction;
          this.state.motion = (direction == 'left') ? -1 : 1;
        }
      };

      // Ganondorf events
      ganondorf.on('tick', function(evt) {
        var self = this,
          bounds = self.getBounds(),
          state = ganondorfLogic.state;

        // Move sprite registration point to center
        self.regX = bounds.width/2;
        self.regY = bounds.height/2;

        // (x, y) coordinates
        self.x += state.motion*state.speed;
        self.y = Math.max(Math.min(self.y + 10,
            stage.height/2 - bounds.height/2),
          -stage.height/2 + bounds.height/2);

        // Left/Right flip depending on direction
      });
      // ...key events
      keyboard.on('left', function() {
        ganondorfLogic.move('left');
      });
      keyboard.on('right', function() {
        ganondorfLogic.move('right');
      });
      keyboard.on('up', function() {
        // jump
      });

      // Game loop
      _.Ticker.timingMode = _.Ticker.RAF;
      _.Ticker.on('tick', function(evt) {
        stage.update(evt);
      });

      // Keyboard events
      $(document).on('keydown', function(e) {
        // Don't handle if game is paused
        if (_.Ticker.getPaused()) { return; }

        if (e.keyCode == 37) { keyboard.dispatchEvent('left'); }
        else if (e.keyCode == 39) { keyboard.dispatchEvent('right'); }
        else if (e.keyCode == 38) { keyboard.dispatchEvent('up'); }
        else if (e.keyCode == 40) { keyboard.dispatchEvent('down'); }
        else { return true; }

        // Don't handle other keyboard events
        return false;
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
