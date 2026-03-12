from odoo import models, fields, api


class IsoConsent(models.Model):
    _name = 'iso.consent'
    _description = 'Consent Record'

    subject_id = fields.Many2one('res.partner', string='Data Subject')
    purpose = fields.Char(required=True)
    consent_date = fields.Datetime()
    revoked_date = fields.Datetime()
    status = fields.Selection([('active', 'Active'), ('revoked', 'Revoked')], default='active')
    source = fields.Char(help='Source or evidence reference')

    def revoke(self):
        self.status = 'revoked'
        from odoo import fields as f
        self.revoked_date = f.Datetime.now()

    @api.model
    def create_from_partner(self, partner, purpose, source=None):
        """Convenience helper to create a consent record for a partner."""
        vals = {
            'subject_id': partner.id,
            'purpose': purpose,
            'consent_date': fields.Datetime.now(),
            'status': 'active',
        }
        if source:
            vals['source'] = source
        return self.create(vals)
