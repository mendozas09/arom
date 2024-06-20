# -*- coding: utf-8 -*-
#############################################################################
#
#    Miguel Mendoza.
#
#    Copyright (C) 2023-TODAY Miguel Mendoza.
#    Author: Miguel Mendoza
#
#    You can modify it under the terms of the GNU AFFERO
#    GENERAL PUBLIC LICENSE (AGPL v3), Version 3.
#
#
#############################################################################

{
    'name': 'custon_aromitalia',
    'version': '16.0.1.0.1',
    'summary': """ """,
    'description': '',
    "category": " ",
    'author': '',
    'company': '',
    'website': "",
    'depends': ['base', 'stock'],
    'data': [
        # ..........data..............

        # ..........security..........
        'security/ir.model.access.csv',

        # ..........views.............
        'views/custom_view.xml',
        'views/inherit_stock_picking.xml',

        # .........wizard.............
        # 'wizard/',

        # ..........reports............
        # 'reports/layout.xml',


    ],
    'images': [],
    'license': 'AGPL-3',
    'installable': True,
    'auto_install': False,
    'application': False,
}
