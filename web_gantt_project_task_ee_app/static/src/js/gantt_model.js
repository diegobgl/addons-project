odoo.define('web_gantt_project_task_ee_app.gantt_model', function (require) {
"use strict";

var AbstractRenderer = require('web.AbstractRenderer');
var core = require('web.core');
var field_utils = require('web.field_utils');
var time = require('web.time');
var GanttModel = require('web_gantt.GanttModel');
var _lt = core._lt;

	var GanttModelInclude = GanttModel.include({
		init: function () {
			this.gantt = null;
			this._super.apply(this, arguments);
		},

		setScale: function (scale,id) {
			this.gantt.btn_id = id;
			this._setFocusDate(this.gantt.focus_date, scale);
		},
	})

});