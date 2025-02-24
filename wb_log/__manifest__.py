# -*- coding: utf-8 -*-
{
    'name': "Wonderbrands logs",

    'summary': """
        Logs changes made to selected fields of a model, providing a detailed history of modifications.
    """,

    'description': """
        This module enables tracking and logging of changes in specific fields of a selected model within Odoo. Each modification is recorded in a structured log, capturing details such as the old and new values, the user responsible for the change, and the timestamp. This functionality enhances auditing capabilities, ensuring transparency and traceability in data modifications. Ideal for businesses that require detailed change history for compliance, accountability, or analytical purposes.
    """,

    'author': "Wonderbrands Tech Team",
    'website': "http://www.wonnderbrands.com",

    'category': 'Technical',
    'version': '15.0-1.0',

    'depends': ['base'],

    'data': [
        "security/ir.model.access.csv",
        "views/views.xml",
        "views/actions.xml",
        "views/menus.xml"
    ],
}
