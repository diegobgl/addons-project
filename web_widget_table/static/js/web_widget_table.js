odoo.define('web_widget_table', function(require)
{
    var registry = require('web.field_registry'),
        AbstractField = require('web.AbstractField'),
        FieldDataTable = AbstractField.extend({
        className: 'oe_form_field_table',
        supportedFieldTypes: ['char'],
        init: function()
        {
            this._super.apply(this, arguments);
        },
        _render: function()
        {
            this.$el.empty(); 
            var field = this.nodeOptions['field_name'],
                fieldModel = this.record.data[field].model,
                fieldRecordIds = this.record.data[field].res_ids,
                table = `<table><thead><tr>`,
                table_fields = this.nodeOptions['fields'],
                headers = this.nodeOptions['headers'];
                datatable_params = this.nodeOptions['datatable_params'];
            headers.forEach(element => {
                table += '<th>' + element + '</th>';
            });
            table+= `</tr></thead><tbody>`;
            this._rpc({
                model: fieldModel,
                method: 'read',
                args: [fieldRecordIds],
                })
                .then(function(result){
                    Array.from(result).forEach(record => {
                        table+='<tr>'
                        table_fields.forEach(function(key){
                            if(key.includes("date")){
                                local_time= moment.utc(record[key] ).local().format('DD-MM-YYYY H:mm:ss');
                                table += (record[key] ? '<td>' + local_time + '</td>': '<td></td>');
                            }
                            else{
                                table += (record[key] ? '<td>' + record[key] + '</td>': '<td></td>');
                            }      
                        });
                        table+='</tr>'
                    });
                    table+= `</tbody></table>`;
                    this.$el.append(
                        jQuery(table).attr({
                            'id': 'datatable',
                            'class': 'display',
                        })
                    );
                    jQuery('#datatable').DataTable(datatable_params);
                }.bind(this));             
        }
    });
    registry.add('widget_table', FieldDataTable);

    return {
        FieldDataTable: FieldDataTable,        
    }
});
