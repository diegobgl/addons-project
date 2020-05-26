=================
 Product Details
=================

Installation
============

* `Install <https://odoo-development.readthedocs.io/en/latest/odoo/usage/install-module.html>`__ this module in a usual way

Usage
=====

The module adds new fields in the product template form view.
You can select a model and a record which will be stored product details.
To change list of model which contains details you have to inherit the ``_model_selection`` function, for example::

    class ProductTemplate(models.Model):
        _inherit = "product.template"

        def _model_selection(self):
            selection = super(ProductTemplate, self)._model_selection()
            selection += [('product.car', 'Car product')]
            return selection
