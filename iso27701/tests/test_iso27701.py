from odoo.tests.common import TransactionCase


class TestIso27701(TransactionCase):
    def test_create_pii_and_activity(self):
        Pii = self.env['iso.pii.type']
        Act = self.env['iso.processing.activity']

        pii = Pii.create({'name': 'Email', 'examples': 'user@example.com'})
        self.assertTrue(pii.id)

        act = Act.create({
            'name': 'Customer signup',
            'pii_type_ids': [(6, 0, [pii.id])],
            'lawful_basis': 'contract',
            'retention_days': 365,
        })
        self.assertTrue(act.id)
