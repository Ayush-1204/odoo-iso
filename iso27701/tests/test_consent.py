from odoo.tests.common import TransactionCase
from odoo import fields


class TestConsent(TransactionCase):
    def test_create_and_revoke_consent(self):
        Partner = self.env['res.partner']
        Consent = self.env['iso.consent']

        p = Partner.create({'name': 'Bob'})
        cons = Consent.create_from_partner(p, purpose='Marketing', source='signup_form')

        self.assertEqual(cons.status, 'active')
        self.assertTrue(cons.consent_date)

        cons.revoke()
        self.assertEqual(cons.status, 'revoked')
        self.assertTrue(cons.revoked_date)
