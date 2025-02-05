# -*- coding: utf-8 -*-
{
    'name': "WonderBrands Data",

    'summary': """
        Displays the wb data dashboards
    """,

    'description': """
        Displays the wb data dashboards and manages 
        the permissions for them
    """,

    'author': "WonderBrands",
    'website': "https://www.wonderbrands.co",

    'category': 'Customizations',
    'version': '15.0',

    # any module necessary for this one to work correctly
    'depends': ['base', 'web'],

    # always loaded
    'data': [
        "data/groups.xml",
        "views/views.xml",
        "views/actions.xml",
        "views/menus.xml",
        "security/ir.model.access.csv",
        "data/charts.xml",
        "data/data_source.xml",
    ],

    'assets': {
        'web.assets_backend': [
            '/wb_data/static/src/js/DashboardsRoot.js',
            '/wb_data/static/src/css/styles.scss',
        ],

        'web.assets_qweb': [
            '/wb_data/static/src/xml/DashboardsRoot.xml',
        ],
    }
}
