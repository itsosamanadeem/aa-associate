# -*- coding: utf-8 -*-
{
    'name': "Scholarship Management",
    'version': '1.0',
    'summary': """
        Manage Scholarships, Donors, and Donation Tracking for Nasra School
    """,
    'description': """
        This module manages scholarships for Nasra School, including configuration of campus, classes, sections, categories, staff categories, donors, and donor groups.
        It integrates with CRM for donor lead tracking and accounting for payment processing.
    """,
    'sequence': -100,
    'author': "Osama Nadeem",
    'website': "https://www.portfolio.itsosamanadeem.duckdns.org/",
    'category': 'Customizations',
    'version': '0.1',
    'application': True,
    'installable': True,
    'depends': ['sale','crm','contacts','accountant','donor_group','res_partner_inherit'],
    'data': [
        'data/ir_sequence_data.xml',
        'security/scholarship_groups.xml',
        'security/ir.model.access.csv',
        'views/scholarship_view.xml',
        'views/scholarship_staff_category.xml',
        'views/scholarship_section.xml', 
        'views/scholarship_class.xml', 
        'views/scholarship_category.xml',
        'views/scholarship_campus.xml',
        'views/scholarship_lines.xml',
        # 'views/scholarship_tree_view.xml',
        'views/scholarship_stages.xml',
        'views/scholarship_tags.xml',        
        'views/donor_sub_groups.xml',
        'views/scholarship_lines_remarks.xml',
        'views/res_partner.xml',
        'views/menu_item_scholarship.xml',
        # 'views/account_vendor_to_donor_menu_item.xml',
        'views/crm_inherit.xml',
        # 'report/sale_letter_template.xml',
        'report/sale_letter_report.xml',
    ],
    'images': ['static/description/icon.png'],
    'assets': {
        "web.assets_backend": [
            "scholarship/static/src/**/*",
        ],
    },
    'license': 'AGPL-3'
}
