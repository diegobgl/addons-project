odoo.define('smart_screenshots.screenshot', function (require) {
    "use strict";

    var core = require('web.core');
    var _t = core._t;
    var SystrayMenu = require('web.SystrayMenu');
    var Widget = require('web.Widget');
    var rpc = require('web.rpc');


    var ScreenShotsMenu = Widget.extend({
        name: 'screenshot_menu',
        template: 'smart_screenshots.screenshot.new_task',
        events: {
            'click .smart_screenshot_button': '_onScreenshotButton',
        },

        _onScreenshotButton: function () {
            var self = this;
            rpc.query({
                model: 'project.task',
                method: 'get_last_task_id',
                args: [],
            }).then(function (data) {
                if (data['task_id']) {
                    self.do_action({
                        name: _t('Last Task'),
                        type: 'ir.actions.act_window',
                        res_model: 'project.task',
                        views: [[false, 'form']],
                        res_id: data['task_id'],
                        target: 'new',
                    });
                }

            });
        }
    });

    SystrayMenu.Items.push(ScreenShotsMenu);
    return ScreenShotsMenu;
});