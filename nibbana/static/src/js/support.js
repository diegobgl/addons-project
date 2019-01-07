odoo.define('nibbana.support', function (require) {
    "use strict";

    var core = require('web.core');
    var Widget = require('web.Widget');

    var Support = Widget.extend({
        template: 'nibbana.support',

        init: function (parent, value) {
            this._super(parent);
        },

    });

    core.action_registry.add('nibbana.support', Support);
});

odoo.define('nibbana.addons', function (require) {
    "use strict";

    var core = require('web.core');
    var Widget = require('web.Widget');

    var Addons = Widget.extend({
        template: 'nibbana.addons',

        init: function (parent, value) {
            this._super(parent);
        },

    });

    core.action_registry.add('nibbana.addons', Addons);
});



