# -*- coding: utf-8 -*-
{
    'name': "Invoice Request",

    'summary': "Allow customers to request invoices externally",

    'description': """
This module allows a customer (partner) to access an external web page to request
an invoice without needing to log in to Odoo.
    """,

    'author': "avipravianti",
    'website': "https://github.com/avipravianti",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Invoicing',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'sale', 'account', 'website'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/invoice_request_views.xml',
        'views/external_sale_invoice_templates.xml'

    ],
    'assets': {
        'web.assets_frontend': [
            'ap_invoice_request/static/src/js/external_sale_invoice.js'
        ]
    },
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
