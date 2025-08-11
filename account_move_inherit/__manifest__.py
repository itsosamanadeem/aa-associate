# __manifest__.py
{
    'name': 'Invoice Product Attribute Wizard',
    'version': '18.0.1.0.0',
    'summary': 'Opens a wizard to select product attributes/variants when adding products to invoices.',
    'description': """
This module adds a wizard in account.move.line (Invoices) to select product
attributes and variants when a product with variants is chosen, similar to
the Sale Order product configurator.
    """,
    'author': 'Your Name',
    'website': 'https://yourwebsite.com',
    'category': 'Accounting',
    'license': 'LGPL-3',
    'depends': [
        'account',
        'product',
        'sale',
        'test_sale_product_configurators',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/account_move_line_views.xml',
        'wizards/product_attribute_invoice_wizard.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}
