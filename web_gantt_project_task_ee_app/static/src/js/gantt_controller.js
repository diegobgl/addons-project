odoo.define('web_gantt_project_task_ee_app.gantt_controller', function (require) {
"use strict";

var AbstractRenderer = require('web.AbstractRenderer');
var core = require('web.core');
var field_utils = require('web.field_utils');
var time = require('web.time');
var GanttController = require('web_gantt.GanttController');
var config = require('web.config');
var Dialog = require('web.Dialog');
var dialogs = require('web.view_dialogs');
var qweb = core.qweb;


var _lt = core._lt;

	var GanttControllerInclude = GanttController.include({

		renderButtons: function ($node) {
			var self = this;
			if ($node) {
				this.$buttons = $(qweb.render("GanttView.buttons", {'isMobile': config.device.isMobile}));
				this.$buttons.appendTo($node);
				this.$buttons.find('.o_gantt_button_scale').bind('click', function (event) {
					self.$buttons.find('.dropdown_gantt_content').text($(this).text());
					self.$buttons.find('.o_gantt_button_scale').removeClass('active');
					self.$buttons.find(this).addClass('active');
					return self._setScale($(event.target).data('value'),this.id);
				});
				this.$buttons.find('.o_gantt_button_left').bind('click', function () {
					var state = self.model.get();
					self._focusDate(state.focus_date.subtract(1, state.scale));
				});
				this.$buttons.find('.o_gantt_button_right').bind('click', function () {
					var state = self.model.get();
					self._focusDate(state.focus_date.add(1, state.scale));
				});
				this.$buttons.find('.o_gantt_button_today').bind('click', function () {
					self.model.setFocusDate(moment(new Date()));
					return self.reload();
				});
			}
		},

		_setScale: function (scale,id) {
			var self = this;
			this.model.setScale(scale,id);
			this.reload().then(function () {
				self.set('title', self.displayName + ' (' + self.model.get().date_display + ')');
			});
		},
	})

});
