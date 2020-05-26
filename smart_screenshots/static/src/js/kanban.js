odoo.define('smart_screenshots.kanban', function (require) {
    "use strict";

    var KanbanRecord = require('web.KanbanRecord');
    var DocumentViewer = require('mail.DocumentViewer');
    var rpc = require('web.rpc');

    KanbanRecord.include({
        events: _.defaults({
            'click .kanban_screenshot_card': '_onKanbanScreenshotCardClick',
        }, KanbanRecord.prototype.events),

        _onKanbanScreenshotCardClick: function (event) {
            if ($(event.target).hasClass('kanban_screenshot_card')) {
                var self = this;
                var task_id;
                if (this.record.problem_task_id.raw_value) {
                    task_id = this.record.problem_task_id.raw_value;
                } else if (this.record.solution_task_id.raw_value) {
                    task_id = this.record.solution_task_id.raw_value;
                }

                var activeAttachmentID = this.record.attachment_id.raw_value;
                var fields = ['filename', 'id', 'mimetype', 'name', 'url'];
                var domain = [['res_id', '=', task_id], ['mimetype', '=', 'image/png']];
                rpc.query({
                    model: 'ir.attachment',
                    method: 'search_read',
                    args: [domain, fields]
                }).then(function (attachments) {
                    if (activeAttachmentID) {
                        var attachmentViewer = new DocumentViewer(self, attachments, activeAttachmentID);
                        attachmentViewer.appendTo($('body'));
                    }
                });
            }
        }
    })
});
