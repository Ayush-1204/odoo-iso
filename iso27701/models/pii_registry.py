from odoo import models, fields, api
from datetime import datetime, timedelta
import logging

_logger = logging.getLogger(__name__)


class IsoPiiType(models.Model):
    _name = 'iso.pii.type'
    _description = 'PII Type'

    name = fields.Char(required=True)
    description = fields.Text()
    examples = fields.Text(string='Examples')


class IsoProcessingActivity(models.Model):
    _name = 'iso.processing.activity'
    _description = 'Processing Activity'

    name = fields.Char(required=True)
    pii_type_ids = fields.Many2many('iso.pii.type', string='PII Types')
    purpose = fields.Text()
    lawful_basis = fields.Selection([
        ('consent', 'Consent'),
        ('contract', 'Contract'),
        ('legal', 'Legal obligation'),
        ('legitimate', 'Legitimate interests'),
    ], required=True, default='legitimate')
    retention_days = fields.Integer(help='Retention period (days)')
    controller_id = fields.Many2one('res.users', string='Controller')
    processor_id = fields.Many2one('res.partner', string='Processor')
    # Retention automation
    target_model = fields.Char(help='Technical model name to apply retention to (e.g. res.partner)')
    date_field = fields.Char(help='Datetime field on target model to compare (e.g. create_date)')
    allow_auto_delete = fields.Boolean(default=False, help='Allow automated deletion when retention is exceeded')

    @api.constrains('retention_days')
    def _check_retention_positive(self):
        for rec in self:
            if rec.retention_days and rec.retention_days < 0:
                raise models.ValidationError('Retention days must be zero or positive')

    @api.constrains('retention_days', 'target_model', 'date_field', 'allow_auto_delete')
    def _check_retention_configuration(self):
        for rec in self:
            if rec.allow_auto_delete and rec.retention_days and not (rec.target_model and rec.date_field):
                raise models.ValidationError('Auto-delete requires `target_model` and `date_field` to be set')

    def run_retention_cleanup(self):
        """
        Find records on `target_model` where `date_field` is older than `retention_days` and unlink them.
        Runs only for activities with `allow_auto_delete` enabled.
        """
        activities = self.search([('allow_auto_delete', '=', True), ('retention_days', '>', 0)])
        for act in activities:
            if not act.target_model or not act.date_field:
                _logger.warning('Skipping activity %s: missing target_model or date_field', act.id)
                continue
            try:
                model = self.env[act.target_model]
            except Exception:
                _logger.exception('Invalid target model for activity %s: %s', act.id, act.target_model)
                continue
            # compute threshold
            try:
                cutoff = (datetime.utcnow() - timedelta(days=act.retention_days)).strftime('%Y-%m-%d %H:%M:%S')
            except Exception:
                _logger.exception('Error computing cutoff for activity %s', act.id)
                continue
            domain = [(act.date_field, '<', cutoff)]
            try:
                records = model.search(domain)
                if records:
                    count = len(records)
                    # Perform unlink with caution
                    records.unlink()
                    _logger.info('Retention cleanup: removed %s records from %s for activity %s', count, act.target_model, act.id)
            except Exception:
                _logger.exception('Error running retention cleanup for %s', act.target_model)
