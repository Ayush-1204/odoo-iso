from odoo import models, fields


class IsoProcessor(models.Model):
    _name = 'iso.processor'
    _description = 'Third-party Processor'

    name = fields.Char(required=True)
    contact = fields.Char()
    contract_reference = fields.Char()
    country = fields.Char()
    data_types = fields.Text(help='Types of personal data processed')
