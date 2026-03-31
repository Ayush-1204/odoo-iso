from odoo import models, fields, api


class IsoConsent(models.Model):
    # Consent ledger used to demonstrate lawful-basis tracking and revocation.
    _name = 'iso.consent'
    _description = 'Consent Record'

    # Link to the data subject (partner) for whom consent is recorded.
    subject_id = fields.Many2one('res.partner', string='Data Subject')
    # Processing purpose (for example: marketing, analytics, support).
    purpose = fields.Char(required=True)
    # Timestamp when consent became effective.
    consent_date = fields.Datetime()
    # Timestamp of withdrawal/revocation, if any.
    revoked_date = fields.Datetime()
    # Lifecycle status for policy enforcement and reporting.
    status = fields.Selection([('active', 'Active'), ('revoked', 'Revoked')], default='active')
    # Evidence pointer (form id, URL, ticket id, document reference, etc.).
    source = fields.Char(help='Source or evidence reference')

    def revoke(self):
        # Minimal state transition helper used by UI actions/automations.
        self.status = 'revoked'
        from odoo import fields as f
        self.revoked_date = f.Datetime.now()

    @api.model
    def create_from_partner(self, partner, purpose, source=None):
        """Convenience helper to create a consent record for a partner."""
        # Keep record creation centralized so defaults are consistent.
        vals = {
            'subject_id': partner.id,
            'purpose': purpose,
            'consent_date': fields.Datetime.now(),
            'status': 'active',
        }
        # Source is optional to support lightweight demo/test data.
        if source:
            vals['source'] = source
        return self.create(vals)
