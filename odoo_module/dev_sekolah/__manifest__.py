{
    'name': 'Dev Sekolah',
    'version': '17.0.1.0.0',
    'summary': 'Model Sekolah/Kelas, computed field, inherit res.partner, smart button',
    'author': 'Avi',
    'license': 'LGPL-3',
    'depends': ['base'],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/dev_sekolah_views.xml',
        'views/res_partner_views.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'dev_sekolah/static/src/kelas_summary/kelas_summary.js',
            'dev_sekolah/static/src/kelas_summary/kelas_summary.xml',
        ],
    },
    'application': True,
    'installable': True,
}
