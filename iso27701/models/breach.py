from odoo import models, fields


class IsoBreach(models.Model):
    # Incident record for personal-data breaches.
    _name = 'iso.breach'
    _description = 'Personal Data Breach'

    name = fields.Char(required=True)
    detected_date = fields.Datetime()
    description = fields.Text()
    affected_data = fields.Text()
    affected_count = fields.Integer()
    # Lightweight lifecycle from intake to closure.
    state = fields.Selection([('draft','Draft'),('investigating','Investigating'),('notified','Notified'),('closed','Closed')], default='draft')

    def action_investigate(self):
        # Begin incident triage/analysis.
        self.state = 'investigating'

    def action_notify(self):
        # Mark that notification workflow has been executed.
        self.state = 'notified'

    def action_close(self):
        # Final state after corrective actions and documentation.
        self.state = 'closed'
