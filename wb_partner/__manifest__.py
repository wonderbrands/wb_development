# -*- coding: utf-8 -*-
{
    'name': "Modificaciones Formulario de Contacto",

    'summary': """
        Modificaciones al formulario de contacto para uso general e interno""",

    'description': """
        Este módulo agrega diferentes modificaciones y campos al formulario de contacto que servirán al registro e identificación de proveedores
        
        -Monto mínimo
        -Días de crédito
        -Días de Compra
        -Unidad de compra
        -Leadtime
    """,

    'author': "WonderBrands",
    'website': "https://wonderbrands.co/",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Inventory',
    'version': '15.0',

    # any module necessary for this one to work correctly
    'depends': ['base',
                'product',
                'sale',
                'stock'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/res_partner_views.xml',
        'views/views.xml',
        'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
