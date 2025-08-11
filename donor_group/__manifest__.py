# -*- coding: utf-8 -*-
{
    'name': "Donor Management",
    'version': '1.0',
    'summary': """
        Donors, and Donation Tracking for Nasra School
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
    'depends': ['base','crm','contacts'],
    'data': [
        'security/ir.model.access.csv',
        'views/donor_group.xml',
    ],
    # 'images': ['static/description/icon.png'],
    'assets': {},
    'license': 'AGPL-3'
}
