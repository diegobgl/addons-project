odoo.define("nibbana.tree_reload", function (require) {
  "use strict";

  var core = require('web.core');
  var ListView = require('web.ListView');
  var bus = require('bus.bus').bus;

  var bus_channel = 'tree_reload';
  bus.add_channel(bus_channel);
  bus.start_polling();

  var ChannelList = ListView.extend({

      init: function() {
        this._super.apply(this, arguments);
        var self = this;
        if (this.model.indexOf('nibbana') != -1) {
          bus.on("notification", this, function() {
            console.log('Reload');
            self.reload();
          });
        }
      },
    });
  });
