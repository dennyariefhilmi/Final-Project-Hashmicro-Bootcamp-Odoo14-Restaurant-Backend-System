# -*- coding: utf-8 -*-
{
    'name': "restaurant",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "My Company",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',
    'application' : True,

    # any module necessary for this one to work correctly
    'depends': ['base', 'mail', 'report_xlsx'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/views.xml',
        'data/data.xml',
        'wizard/pembatalan.xml',
        'wizard/tambah_bahan.xml',
        'wizard/tambah_inventory.xml',
        'views/templates.xml',
        'views/menu.xml',
        'views/inventory.xml',
        'views/bahan_makanan.xml',
        'views/supplier.xml',
        'views/menu_makanan.xml',
        'views/order.xml',
        'views/member.xml',
        'views/antrian.xml',
        'views/karyawan.xml',
        'views/delivery.xml'




    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
