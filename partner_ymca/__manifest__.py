# -*- coding: utf-8 -*-
{
    'name': "custom_addons/partner_ymca",

    'description': """
        adapts the business pattern for YMCA
    """,

    'author': "Cesar Gutierrez",
    'website': "cesareomargtz@gmail.com",

    'category': 'Uncategorized',
    'version': '0.1',

    'depends': ['base', 'product'],

    'data': [
        # 'security/ir.model.access.csv',
        'views/resources.xml',
        'views/partner_ymca.xml',
        'views/partner_ymca_code.xml',
        'views/partner_ymca_locker.xml',
        'views/product_ymca.xml',
    ],

    'demo': [
        'demo/demo.xml',
    ],
}
