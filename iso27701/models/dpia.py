from odoo import models, fields


class IsoDpia(models.Model):
    _name = 'iso.dpia'
    _description = 'Data Protection Impact Assessment (DPIA)'

    name = fields.Char(required=True)
    project = fields.Char()
    personal_data = fields.Text(help='Types of personal data involved')
    risk_level = fields.Selection([('low','Low'),('medium','Medium'),('high','High')], default='medium')
    impact = fields.Text()
    mitigations = fields.Text()
    approved = fields.Boolean(default=False)

    def action_approve(self):
        self.approved = True
