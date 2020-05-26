odoo.define('web_gantt_project_task_ee_app.gantt_renderer', function (require) {
"use strict";

var AbstractRenderer = require('web.AbstractRenderer');
var core = require('web.core');
var field_utils = require('web.field_utils');
var time = require('web.time');
var GanttRenderer = require('web_gantt.GanttRenderer');
var _lt = core._lt;

	var GanttRendererInclude = GanttRenderer.include({

		_ganttContainer: function (ganttTasks) {
			// horrible hack to make sure that something is in the dom with the required id.  The problem is that
			// the action manager renders the view in a document fragment. More explaination : GED
			var temp_div_with_id;
			if (this.$div_with_id){
				temp_div_with_id = this.$div_with_id;
			}
			this.$div_with_id = $('<div>').attr('id', this.chart_id);
			this.$div_with_id.wrap('<div></div>');
			this.$div = this.$div_with_id.parent();
			this.$div.prependTo(document.body);

			// Initialize the gantt chart
			while (this.gantt_events.length) {
				gantt.detachEvent(this.gantt_events.pop());
			}
			this._scaleZoom(this.state.scale,this.state);
			gantt.init(this.chart_id);
			gantt._click.gantt_row = undefined; // Remove the focus on click

			gantt.clearAll();
			gantt.showDate(this.state.focus_date);
			gantt.parse({"data": ganttTasks});
			gantt.sort(function (a, b){
				if (gantt.hasChild(a.id) && !gantt.hasChild(b.id)){
					return -1;
				} else if (!gantt.hasChild(a.id) && gantt.hasChild(b.id)) {
					return 1;
				} else if (a.index > b.index) {
					return 1;
				} else if (a.index < b.index) {
					return -1;
				} else {
					return 0;
				}
			});

			// End of horrible hack
			var scroll_state = gantt.getScrollState();
			this.$el.empty();
			this.$el.append(this.$div.contents());
			gantt.scrollTo(scroll_state.x, scroll_state.y);
			this.$div.remove();
			if (temp_div_with_id) temp_div_with_id.remove();
		},

		_scaleZoom: function (value,state) {
			gantt.config.step = 1;
			gantt.config.min_column_width = 50;
			gantt.config.scale_height = 50;
			var today = new Date();

			function css(date) {
				if(date.getDay() === 0 || date.getDay() === 6) return "weekend_scale";
				if(date.getMonth() === today.getMonth() && date.getDate() === today.getDate()) return "today";
			}
			switch (value) {
				case "day":
					if(state.btn_id == 'half_day')
					{
						gantt.templates.scale_cell_class = css;
						gantt.config.scale_unit = "day";
						gantt.config.date_scale = "%d %M";
						gantt.config.subscales = [{unit:"hour", step:12, date:"%H h"}];
						gantt.config.scale_height = 27;
						break;
					}
					else if(state.btn_id == 'qtr_day')
					{
						gantt.templates.scale_cell_class = css;
						gantt.config.scale_unit = "day";
						gantt.config.date_scale = "%d %M";
						gantt.config.subscales = [{unit:"hour", step:6, date:"%H h"}];
						gantt.config.scale_height = 27;
						break;
					}
					else{
						gantt.templates.scale_cell_class = css;
						gantt.config.scale_unit = "day";
						gantt.config.date_scale = "%d %M";
						gantt.config.subscales = [{unit:"hour", step:1, date:"%H h"}];
						gantt.config.scale_height = 27;
						break;
					}
				   
				case "week":
					var weekScaleTemplate = function (date){
						var dateToStr = gantt.date.date_to_str("%d %M %Y");
						var endDate = gantt.date.add(gantt.date.add(date, 1, "week"), -1, "day");
						return dateToStr(date) + " - " + dateToStr(endDate);
					};
					gantt.config.scale_unit = "week";
					gantt.templates.date_scale = weekScaleTemplate;
					gantt.config.subscales = [{unit:"day", step:1, date:"%d, %D", css:css}];
					break;
				case "month":
					gantt.config.scale_unit = "month";
					gantt.config.date_scale = "%F, %Y";
					gantt.config.subscales = [{unit:"day", step:1, date:"%d", css:css}];
					gantt.config.min_column_width = 25;
					break;
				case "year":
					if(state.btn_id == 'qtr_year')
					{
						gantt.config.scale_unit = "year";
						gantt.config.date_scale = "%Y";
						gantt.config.subscales = [{unit:"month", step:3, date:"%M"}];
						break;
					}
					else if(state.btn_id == 'half_year')
					{
						gantt.config.scale_unit = "year";
						gantt.config.date_scale = "%Y";
						gantt.config.subscales = [{unit:"month", step:6, date:"%M"}];
						break;
					}
					else{
						gantt.config.scale_unit = "year";
						gantt.config.date_scale = "%Y";
						gantt.config.subscales = [{unit:"month", step:1, date:"%M"}];
						break;
					}
					
			}
		},
	})

});