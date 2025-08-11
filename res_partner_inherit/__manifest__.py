# -*- coding: utf-8 -*-
{
    'name': "Res Partner Inherit",
    'version': '1.0',
    'summary': """
        Res Partner Inherit
    """,
    'sequence': -100,
    'author': "Osama Nadeem",
    'website': "https://www.portfolio.itsosamanadeem.duckdns.org/",
    'category': 'Customizations',
    'version': '0.1',
    'application': True,
    'installable': True,
    'depends': ['contacts','donor_group'],
    'data': [
        'views/res_partner.xml',
    ],
    # 'images': ['static/description/icon.png'],
    'assets': {},
    'license': 'AGPL-3'
}
