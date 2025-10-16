
{
    'name': 'yousentech_inventory_default',
    'category': 'Inventory',
    'summary': """""",
    'description': """""",
    'author': 'yousen tech Techno Solutions, Odoo SA',
    'website': "https://www.qimamhd.com",
    'company': 'yousen Techno Solutions',
    'maintainer': 'yousen Techno Solutions',
    'depends': ['base', 'sale','purchase','account', 'stock','sale_management','yousentech_inventory'],
    'data': [
        'security/ir.model.access.csv',
        'views/res_user.xml',
        'views/res_company.xml',
        'views/purchase_order.xml',
        'views/stock_picking.xml',
         # 'views/sale_order.xml'
    ],
    'images': ['static/description/icon.png'],
    'license': 'LGPL-3',
    'images': [],
    'sequence': '-100',
    'installable': True,
    'auto_install': False,
    'application': True,
}
