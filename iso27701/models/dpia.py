from odoo import models, fields


class IsoDpia(models.Model):
    # DPIA register entry capturing risk/mitigation for a project/process.
    _name = 'iso.dpia'
    _description = 'Data Protection Impact Assessment (DPIA)'

    name = fields.Char(required=True)
    project = fields.Char()
    personal_data = fields.Text(help='Types of personal data involved')
    # Coarse risk band to support fast triage and dashboard reporting.
    risk_level = fields.Selection([('low','Low'),('medium','Medium'),('high','High')], default='medium')
    impact = fields.Text()
    mitigations = fields.Text()
    approved = fields.Boolean(default=False)

    def action_approve(self):
        # Approval flag can be used by downstream workflows/reports.
        self.approved = True
