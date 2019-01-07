odoo.define('nibbana.tour', function (require) {
'use strict';

var core = require('web.core');
var tour = require('web_tour.tour');

var _t = core._t;

tour.register('project_activation', {
    url: '/web',
},
    [
        {
        trigger: '.oe_form_field_status.oe_form_status_clickable.o_nibbana_project_statusbar.o_form_field',
        content: _t('Here you change state of your project.'),
        position: 'left',
        },
        {
        //trigger: 'i[class="fa fa-toggle-on"]',
        trigger: 'i[class="fa fa-toggle-on"]',
        content: _t('Click here to deactivate your project.'),
        position: 'top',
        },
    ]
);

});