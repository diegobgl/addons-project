odoo.define('web_gantt_project_task_app.gantt_renderer', function (require) {
"use strict";

var BasicRenderer = require('web.BasicRenderer');
var config = require('web.config');
var core = require('web.core');
var dom = require('web.dom');
var AbstractRenderer = require('web.AbstractRenderer');
var dialogs = require('web.view_dialogs');

var _t = core._t;
var qweb = core.qweb;
var rpc = require('web.rpc');

	return AbstractRenderer.extend({
		className: "o_gantt_view",

		init: function () {
			this._super.apply(this, arguments);
		},

		_render: function () {
			this.$el.empty();
			this.show_gantt();
			return $.when();
		},
		
		show_gantt: function () {
			var self = this;			
			$('.o_gantt_view').append("<div id='container' style=' width: 100%;height: 100%;margin: 0;padding: 0;'></div>");
			anychart.onDocumentReady(function () {    
				// create data
				var data = [];
				rpc.query({
					model: 'project.project',
					method: 'get_gantt_data',
					args: [1],
				}, {async: false}).then(function(output) {
					data = output;
				});

				// create a data tree
				var treeData = anychart.data.tree(data, "as-tree");    
				// create a chart
				var chart = anychart.ganttProject();        
				// set the data
				chart.data(treeData);
				// set the container id
				chart.container("container");    
				// initiate drawing the chart
				// chart.background("#64b5f6 0.2");
				chart.rowHoverFill("#ffd54f 0.3");
				chart.rowSelectedFill("#ffd54f 0.3");
				chart.rowStroke("0.5 #64b5f6");
				chart.columnStroke("0.5 #64b5f6");
				// set the row height
				chart.defaultRowHeight(35);
				// set the header height
				// chart.headerHeight(105);
				chart.splitterPosition("15%");

				var dataGrid = chart.dataGrid();
				dataGrid.rowEvenFill("gray 0.3");
				dataGrid.rowOddFill("gray 0.1");
				dataGrid.rowHoverFill("#ffd54f 0.3");
				dataGrid.rowSelectedFill("#ffd54f 0.3");
				dataGrid.columnStroke("2 #64b5f6");
				// dataGrid.headerFill("#64b5f6 0.2");

				// set the text of the second data grid column

				var column_1 = chart.dataGrid().column(0);
					column_1.labels().fontWeight(600);
					column_1.labels().useHtml(true);

					column_1.labels().format(function() {

					  var children = this.item.numChildren();
					  var index = this.linearIndex;

					  // identify the resource type and display the corresponding text
					  if (children > 0) {
						return "<span style='color:#00234f;font-size:13px;'>" + index + ".</span>";
					  } else {
						return "<span style='color:#0d4894;font-size:13px;'>" + index + ".</span>";
					  }
				});

				var column_2 = chart.dataGrid().column(1);    
				column_2.labels().useHtml(true);

				column_2.labels().format(function() {

				  var numChildren = this.item.numChildren();
				  var duration = (this.end - this.start) / 1000 / 3600 / 24;
				  var customField = " ";
				  if (this.getData("custom_field")) {
					customField = "<span style='font-weight:bold;font-size:13px;'>" +
							 this.getData("custom_field") + customField + "</span>";
				  }

				  var parentText = "<span style='color:#00234f;font-weight:bold;font-size:13px;'>" +
								   this.name.toUpperCase() + "<span>";
				  var childText = "<span style='color:#0d4894;font-size:13px;'>" + customField + 
								  this.name + ": " + duration + "</span>";

				  // identify the resource type and display the corresponding text
				  if (numChildren > 0) {
					return parentText;
				  } else {
					return childText;
				  }

				});
				chart.dataGrid().column(1).depthPaddingMultiplier(60);
				// access data grid buttons
				var buttons = chart.dataGrid().buttons();

				// configure data grid buttons
				buttons.fontWeight(600);
				buttons.fontSize(16);
				buttons.fontFamily("Courier");
				buttons.background().fill(null);
				buttons.background().stroke(null);
				buttons.width(30);
				buttons.cursor("default");

				// configure data grid buttons in the normal state
				buttons.normal().content("[+]");
				buttons.normal().fontColor("#ef6c00");

				// configure data grid buttons in the hover state
				buttons.hovered().content("[+]");
				buttons.hovered().fontColor(anychart.color.lighten("#ef6c00"));

				// configure data grid buttons in the selected state
				buttons.selected().content("[-]");
				buttons.selected().fontColor("#64b5f6");

				chart.getTimeline().tooltip().useHtml(true);    
				chart.getTimeline().tooltip().format(
				  "<span style='font-weight:600;font-size:12pt'>" +
				  "{%start}{dateTimeFormat:dd MMM} – " +
				  "{%end}{dateTimeFormat:dd MMM}</span><br><br>" 
				);

				chart.draw();    
				// fit elements to the width of the timeline
				chart.fitAll();
			});    
		},

	});

});