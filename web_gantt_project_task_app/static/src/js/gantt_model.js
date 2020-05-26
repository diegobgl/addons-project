odoo.define('web_gantt_project_task_app.gantt_model', function (require) {
"use strict";

var AbstractModel = require('web.AbstractModel');

	return AbstractModel.extend({
	    init: function () {
	        this._super.apply(this, arguments);
	        this.gantt = null;
	    },
	});
});