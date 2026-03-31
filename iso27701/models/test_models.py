from odoo import models, fields


class IsoTestRetention(models.Model):
    # Dedicated test fixture model used by retention cleanup tests.
    _name = 'iso.test.retention'
    _description = 'Test model for retention cleanup'

    name = fields.Char(required=True, default='test')
    # Reference timestamp field used by cleanup domain filters.
    ts = fields.Datetime(string='Timestamp', default=fields.Datetime.now)
