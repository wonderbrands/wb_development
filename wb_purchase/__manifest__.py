# -*- coding: utf-8 -*-
{
    'name': "Modificaciones Formulario de Compra",

    'summary': """
        Modificaciones al template de compra para uso general e interno""",

    'description': """
        Este módulo agrega diferentes modificaciones y campos al formulario del producto y a la tabla de compra de productos
        
        -Leadtime
        -Fecha de cita en almacén
        -Fecha prevista
        -Monto mínimo
        -Unidad
        -Días de crédito
        -Días de compra
        -Pedido original
    """,

    'author': "Wonderbrands",
    'website': "https://www.wonderbrands.co",
    'license': 'LGPL-3',
    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Inventory',
    'version': '15.0',

    # any module necessary for this one to work correctly
    'depends': ['base',
                'product',
                'sale',
                'stock',
                'wb_product'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/purchase_order_line_views.xml',
        'views/purchase_order_views.xml',
        'views/views.xml',
        'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
