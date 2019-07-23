# -*- coding: utf-8 -*-
{
    'name': "ymca_income_vaoucher",

    'author': "Cesar Gtz",
    'website': "cesargtz.mx",

    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','account_voucher', 'account'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/resources.xml',
        'views/report_ymca_voucher.xml',
        'views/ymca_income.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
