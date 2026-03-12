from odoo.tests.common import TransactionCase
from odoo import fields


class TestDsrWorkflow(TransactionCase):
    def test_dsr_state_transitions_and_verify(self):
        Dsr = self.env['iso.dsr']

        dsr = Dsr.create({
            'requestor_name': 'Alice',
            'requestor_email': 'alice@example.com',
            'request_type': 'access',
        })

        self.assertEqual(dsr.state, 'draft')

        # verify should set verified_date and open
        dsr.action_verify()
        self.assertEqual(dsr.state, 'open')
        self.assertTrue(dsr.verified_date)
        self.assertTrue(dsr.verifier_id)

        # complete
        dsr.action_done()
        self.assertEqual(dsr.state, 'done')
