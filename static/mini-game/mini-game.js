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

      // Keyboard event dispatchers (use to bind key events)
      var keydown = new _.EventDispatcher(),
        keyup = new _.EventDispatcher();
      // ... keyboard state
      var keyboard = {};

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

      // Ganondorf object
      var ganondorf = {
        display: null,
        sprites: {
          left: new _.Sprite(ganondorfSS['left'], 'idle'),
          right: new _.Sprite(ganondorfSS['right'], 'idle')
        },
        state: {
          direction: null,
          motion: 0,
          speed: 3
        }
      };
      // ...display container
      (function(sprites) {
        var cont = new _.Container();
        cont.addChild(sprites.left).visible = false;
        cont.addChild(sprites.right).visible = true;
        stage.addChild(cont);
        ganondorf.display = cont;
      }) (ganondorf.sprites);

      // Ganondorf events
      ganondorf.display.on('tick', function(evt) {
        var self = this,
          bounds = self.getBounds(),
          state = ganondorf.state;

        // Continuous events
        state.motion = 0;
        if (keyboard.left) { state.motion -= 1; }
        if (keyboard.right) { state.motion += 1; }

        // Move sprite registration point to center
        self.regX = bounds.width/2;
        self.regY = bounds.height/2;

        // (x, y) coordinates
        self.x += state.motion*state.speed;
        self.y = Math.max(Math.min(self.y + 10,
            stage.height/2 - bounds.height/2),
          -stage.height/2 + bounds.height/2);

        // Direction change
        if (state.motion != 0) {
          if (keyboard.left) {
            state.direction = 'left';
          } else {
            state.direction = 'right';
          }
        }

        // Left/Right sprite selection
        (function(sprites) {
          if (state.direction == 'left') {
            sprites.left.visible = true;
            sprites.right.visible = false;
          } else {
            sprites.left.visible = false;
            sprites.right.visible = true;
          }
        }) (ganondorf.sprites);
      });
      keydown.on('up', function() {
        // jump
      });

      // Game loop
      _.Ticker.timingMode = _.Ticker.RAF;
      _.Ticker.on('tick', function(evt) {
        stage.update(evt);
      });

      // Keyboard events
      (function() {
        // Codes to handle
        var codes = {
          left: 37,
          right: 39,
          up: 38,
          down: 40
        };

        $(document).on('keydown', function(e) {
          // Don't handle if game is paused
          if (_.Ticker.getPaused()) { return; }

          for (var key in codes) {
            if (codes[key] != e.keyCode) { continue; }
            if (keyboard[key] === false) { keydown.dispatchEvent(key); }
            keyboard[key] = true;
            return false;
          }
        }).on('keyup', function(e) {
          // Don't handle if game is paused
          if (_.Ticker.getPaused()) { return; }

          for (var key in codes) {
            if (codes[key] != e.keyCode) { continue; }
            if (keyboard[key] === true) { keyup.dispatchEvent(key); }
            keyboard[key] = false;
            return false;
          }
        });
      }) ();
    }) ('mini-game-canvas', createjs);

    // UI integration
    $('#mini-game-toggle').on('click', function() {
      var _ = createjs;
      _.Ticker.setPaused(!_.Ticker.getPaused());
      $('#mini-game-canvas').parents().first().slideToggle(500);
    });
  });
}) (jQuery);
