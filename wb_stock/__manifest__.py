# -*- coding: utf-8 -*-
{
    'name': "Modificaciones Formulario de Traslados",

    'summary': """
        Modificaciones al template de traslados para uso general e interno""",

    'description': """
        Este módulo agrega diferentes modificaciones y campos al formulario de traslados
        
        -Fecha de cita en almacén
    """,

    'author': "Wonderbrands",
    'website': "https://www.wonderbrands.co",
    'license': 'LGPL-3',
    'category': 'Inventory',
    'version': '15.0',

    # any module necessary for this one to work correctly
    'depends': ['base',
                'product',
                'sale',
                'stock'],

    # always loaded
    'data': [
        #'security/ir.model.access.csv',
        'views/stock_picking_views.xml',
        'views/views.xml',
        'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
