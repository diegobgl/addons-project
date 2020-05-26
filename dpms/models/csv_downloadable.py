#-*- coding:utf-8 -*-

from odoo import models, fields, api, http


#
# @http.route('/csv/download/<int:rec_id>/', auth='user', website=True)
# def csvdownload(self, rec_id, **kw):
#     return http.request.env['your_addon.your_model']._csv_download({'rec_id': rec_id})

# class MyModel(models.Model):
#     def _get_csv_url(self):
#         self.csv_url = "/csv/download/{}/".format(self.id)
#
#     csv_url = fields.Char(compute=_get_csv_url)
#
#     @api.model
#     def _csv_download(self, vals):
#         sql = """SELECT
#                      quote_nullable(field_1),
#                      quote_nullable(field_2),
#                      quote_nullable(field_3),
#                      quote_nullable(field_4)
#                  FROM
#                      table_name
#                  WHERE id={}""".format(vals.get(rec_id))
#         self.env.cr.execute(sql)
#         rows = self.env.cr.fetchall()
#         csv = """'Field 1','Field 2','Field 3','Field 4'\n"""
#         if rows:
#             for row in rows:
#                 csv_row = ""
#                 for item in row:
#                     csv_row += "{},".format(item)
#                 csv += "{}\n".format(csv_row[:-1])
#         return csv

# <a id="csv_download" href="#" target="_blank" download="file.csv"/>
#
# <div id="csv_url_div" style="display:none"><field name="csv_url"/></div>
#
# <script>
# $(document).ready(function(){
#     var csv_url = $("#csv_url_div").text();
#     $("#csv_download").attr("href", csv_url);
# });
# </script>