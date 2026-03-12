from odoo import models, fields


class IsoTestRetention(models.Model):
    _name = 'iso.test.retention'
    _description = 'Test model for retention cleanup'

    name = fields.Char(required=True, default='test')
    ts = fields.Datetime(string='Timestamp', default=fields.Datetime.now)
