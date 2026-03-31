{
    # Module metadata used by Odoo app registry.
    'name': 'ISO27701 - Privacy Information Management',
    'version': '17.0.1.0.0',
    'summary': 'RoPA, Processing Activities, DSAR, Consent, DPIA, Breach management',
    'category': 'Security',
    'author': 'FOCUZ AI',
    'website': 'https://www.focuz.io',
    'license': 'AGPL-3',
    # Dependencies provide foundational models, mail dispatch, and security/audit addons.
    'depends': ['base','mail','auditlog','base_user_role','password_security','auth_session_timeout'],
    'data': [
        # Access rules for new models.
        'security/ir.model.access.csv',
        # Main UI menus, views, and actions.
        'views/iso27701_views.xml',
        # Markdown source that powers the mapping CSV export endpoint.
        'data/iso27701_mapping.md',
        # Scheduled cleanup and automation jobs.
        'data/ir_cron.xml',
        # Mail template for DSR verification flow.
        'data/mail_template_dsr.xml',
    ],
    'installable': True,
    'application': False,
}
