# D7 SMS Gateway
[![License: AGPL v3](https://img.shields.io/badge/License-AGPL%20v3-blue.svg)](https://www.gnu.org/licenses/agpl-3.0)

D7SMS Gateway integration will help you to easily communicate with your customers or employees by SMS from within your Odoo Account. This integration will power your Odoo platform for Worldwide SMS Transmission using D7's own connectivity to Global Mobile Network Operators

# Basic Features!
  - Send direct personalized Individual or Bulk messages from SMS Module
  -  Integrated Reports for Delivery Status and Message history within Odoo Platform.
  - Templates for each section can be defined by Administrator.
  - Enable or Disable SMS Feature for each module.
  - Cost effective Communication with High Reliability.


# Applicable modules and Features
- Project: Notify contacts or customers about Project tasks creation and updating on each stage.
- Purchase: Purchase order confirmation will be sent automatically by SMS.
- Sale: Get SMS Alerts on the Sales order confirmation.
- Payroll: Receive SMS Alerts when payroll is confirmed.
- Leaves: Notify employee by SMS about their Leave Allocation & Approval status.


You can also:
  - Configure and setup the SMS and templates in module wise
  - Enable access rights to restrict SMS views for system users
  - Create and edit the SMS templates, by using reserved words



#### Reserved Words [For SMS Templates]
>The SMS templates can be created without knowing any technical knowledge by using some reserved words. Either you can use the demo templates with the module or create a new one using the reserved words.

| Code | Definition | Module |
| ------ | ------ | ------ |
| {name} | Name of person who receive SMS | General
| {type} | Leave / Allocation Request | HRMS Leaves
| {days} | Leave Days | HRMS Leaves
| {duration} | Duration/Period | HRMS Leaves Duration / HRMS Payroll Period
| {payslip_name} | Payslip Name | HRMS Payroll
| {p_reference} | Payslip Reference | HRMS Payroll
| {manager} | Manager | General
| {so_order} | Sale Order | Sales
| {po_order} | Purchase Order | Purchase
| {amount} | Total Amount | Sales / Purchase
| {amount_words} | Amount in words | Sales / Purchase
| {project} | Project | Project
| {stage} | Project Stage | Project
| {task} | Project Tasks | Project

### Tech

* [PYTHON](https://www.python.org/) - Models
* [XML](https://www.w3.org/XML/) - Views
* [HTML](https://www.w3.org/html/) - UI
* [Twitter Bootstrap](http://getbootstrap.com/2.3.2/) - UI
* [backbone.js](http://backbonejs.org/) - Views
* [jQuery](https://jquery.com/)

### Todos

 -
 ### Installation

Install the [Odoo11](https://github.com/odoo/odoo/tree/11.0) and dependency modules defined in manifest. After installation you can configure details under general settings or under the menu SMS.

### Recommends community version and enterprise editions !

### Contact
>DIRECT7 NETWORKS
a SIGNTAPER FZCompany
DTEC, TECHNO-HUB2
Dubai Silicon Oasis
Dubai - U.A.E.
website: http://d7networks.com/

### Bug Tracker and support
* Support Email <odoo@d7networks.com>
* GitHub [issues]()

License
----
[![License: AGPL v3](https://img.shields.io/badge/License-AGPL%20v3-blue.svg)](https://www.gnu.org/licenses/agpl-3.0)