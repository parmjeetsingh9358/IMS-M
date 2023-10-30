# -*- coding: utf-8 -*-

{
    'name': "HSPL Appointment Booking",

    'summary': """HSPL Appointment Booking""",

    'author': 'Heliconia Solutions Pvt. Ltd.',

    'category': 'Tools',

    'website': 'https://heliconia.io',

    'version': "16.0.0.1.0",
    "license": "OPL-1",
    'depends': ['base','website', 'calendar', 'resource_booking'],


    'data': [
        'views/appointment_templates.xml',
        'views/resource_booking_view_inherit.xml',

    ],

    'installation': True,
    'application': True,
    'auto_install': False,

}
