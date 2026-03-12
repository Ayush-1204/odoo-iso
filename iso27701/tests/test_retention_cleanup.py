from odoo.tests.common import TransactionCase
from odoo import fields
from datetime import timedelta


class TestRetentionCleanup(TransactionCase):
    def test_retention_cleanup_removes_old_records(self):
        Ret = self.env['iso.test.retention']
        Act = self.env['iso.processing.activity']

        # create one old and one recent record
        now = fields.Datetime.now()
        old_ts = (fields.Datetime.from_string(now) - timedelta(days=40))
        old_ts_str = fields.Datetime.to_string(old_ts)
        recent_ts = now

        old = Ret.create({'name': 'old', 'ts': old_ts_str})
        recent = Ret.create({'name': 'recent', 'ts': recent_ts})

        # ensure created
        self.assertTrue(old.id)
        self.assertTrue(recent.id)

        # create processing activity that points to this model
        act = Act.create({
            'name': 'Test retention',
            'target_model': 'iso.test.retention',
            'date_field': 'ts',
            'retention_days': 30,
            'allow_auto_delete': True,
            'lawful_basis': 'legitimate',
        })

        # run cleanup
        act.run_retention_cleanup()

        # old should be removed, recent should remain
        remaining = Ret.search([])
        names = remaining.mapped('name')
        self.assertIn('recent', names)
        self.assertNotIn('old', names)
