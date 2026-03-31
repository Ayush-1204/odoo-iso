from odoo import models, fields, api
from odoo.exceptions import ValidationError
import uuid
import logging

_logger = logging.getLogger(__name__)


class IsoDsr(models.Model):
    # Core record for Data Subject Requests (DSAR/DSR workflow).
    _name = 'iso.dsr'
    _description = 'Data Subject Request'

    # Human-readable identifier generated from sequence when available.
    name = fields.Char(readonly=True, default='New')
    requestor_name = fields.Char(required=True)
    requestor_email = fields.Char()
    # Request taxonomy aligned with common privacy rights categories.
    request_type = fields.Selection([
        ('access', 'Access'),
        ('erasure', 'Erasure'),
        ('rectification', 'Rectification'),
        ('portability', 'Portability'),
    ], required=True)
    # Basic lifecycle states for triage and closure.
    state = fields.Selection([
        ('draft', 'Draft'),
        ('open', 'Open'),
        ('done', 'Done'),
        ('refused', 'Refused'),
    ], default='draft')
    activity_id = fields.Many2one('iso.processing.activity', string='Related Processing')
    note = fields.Text()
    created_date = fields.Datetime(readonly=True)
    verified_date = fields.Datetime(readonly=True)
    verifier_id = fields.Many2one('res.users', string='Verified by')

    @api.model
    def create(self, vals):
        # Generate sequence-backed identifier; gracefully fallback when sequence
        # reference is unavailable in lightweight environments.
        vals.setdefault('name', 'DSR/%s' % (self.env['ir.sequence'].next_by_code('iso.dsr') if self.env.ref('iso27701', raise_if_not_found=False) else 'new'))

        # Ensure each request has a verification token for email verification flow.
        if not vals.get('verification_token'):
            vals['verification_token'] = uuid.uuid4().hex

        rec = super().create(vals)
        # Capture creation timestamp explicitly for reporting consistency.
        rec.created_date = fields.Datetime.now()
        return rec

    def generate_verification_token(self):
        # Regenerate token when resending verification or rotating stale token.
        for rec in self:
            rec.verification_token = uuid.uuid4().hex
        return True

    def send_verification_email(self):
        """Send a verification email to the requestor using mail.template.

        This creates a `mail.mail` entry via the mail template; Odoo mail setup
        must be configured to actually send the email.
        """
        template = False
        try:
            # Preferred path: use managed template for localization and branding.
            template = self.env.ref('iso27701.dsr_verification_template')
        except Exception:
            template = False
        for rec in self:
            if not rec.requestor_email:
                _logger.warning('DSR %s missing requestor_email; skipping email', rec.id)
                continue
            if not rec.verification_token:
                rec.generate_verification_token()
            if template:
                try:
                    template.sudo().with_context(lang=rec.env.user.lang).send_mail(rec.id, force_send=False)
                except Exception:
                    _logger.exception('Failed to send verification email for DSR %s', rec.id)
            else:
                # Fallback: create a simple mail.mail record
                try:
                    self.env['mail.mail'].create({
                        'subject': 'Verify your data subject request',
                        'email_from': self.env.user.email_formatted if self.env.user.email_formatted else 'no-reply',
                        'email_to': rec.requestor_email,
                        'body_html': '<p>Please verify your request using token: %s</p>' % rec.verification_token,
                        'model': 'iso.dsr',
                        'res_id': rec.id,
                    })
                except Exception:
                    _logger.exception('Failed to queue mail for DSR %s', rec.id)

    @api.constrains('request_type', 'requestor_email')
    def _check_email_for_certain_requests(self):
        # Access/portability usually require response delivery to requestor.
        for rec in self:
            if rec.request_type in ('access', 'portability') and not rec.requestor_email:
                raise ValidationError('Requestor email is required for access and portability requests')

    def action_open(self):
        # State transition helpers are kept small for UI button actions.
        self.state = 'open'

    def action_done(self):
        self.state = 'done'

    def action_refuse(self):
        self.state = 'refused'

    def action_verify(self):
        """Mark request as verified by current user and open it for processing."""
        for rec in self:
            # Store audit-friendly verification metadata.
            rec.verified_date = fields.Datetime.now()
            rec.verifier_id = self.env.uid
            rec.state = 'open'

