{
    'name': 'ISO27701 - Privacy Information Management',
    'version': '17.0.1.0.0',
    'summary': 'RoPA, Processing Activities, DSAR, Consent, DPIA, Breach management',
    'category': 'Security',
    'author': 'FOCUZ AI',
    'website': 'https://www.focuz.io',
    'license': 'AGPL-3',
    'depends': ['base','mail','auditlog','base_user_role','password_security','auth_session_timeout'],
    'data': [
        'security/ir.model.access.csv',
        'views/iso27701_views.xml',
        'data/iso27701_mapping.md',
        'data/ir_cron.xml',
        'data/mail_template_dsr.xml',
    ],
    'installable': True,
    'application': False,
}
