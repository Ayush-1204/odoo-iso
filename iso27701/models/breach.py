from odoo import models, fields


class IsoBreach(models.Model):
    _name = 'iso.breach'
    _description = 'Personal Data Breach'

    name = fields.Char(required=True)
    detected_date = fields.Datetime()
    description = fields.Text()
    affected_data = fields.Text()
    affected_count = fields.Integer()
    state = fields.Selection([('draft','Draft'),('investigating','Investigating'),('notified','Notified'),('closed','Closed')], default='draft')

    def action_investigate(self):
        self.state = 'investigating'

    def action_notify(self):
        self.state = 'notified'

    def action_close(self):
        self.state = 'closed'
