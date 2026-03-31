from odoo import models, fields


class IsoProcessor(models.Model):
    # Registry of third-party processors/vendors.
    _name = 'iso.processor'
    _description = 'Third-party Processor'

    name = fields.Char(required=True)
    contact = fields.Char()
    contract_reference = fields.Char()
    # Destination country is relevant for transfer-risk analysis.
    country = fields.Char()
    data_types = fields.Text(help='Types of personal data processed')
