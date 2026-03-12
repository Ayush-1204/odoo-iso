from odoo import models, fields, api
from odoo.exceptions import ValidationError
import uuid
import logging

_logger = logging.getLogger(__name__)


class IsoDsr(models.Model):
    _name = 'iso.dsr'
    _description = 'Data Subject Request'

    name = fields.Char(readonly=True, default='New')
    requestor_name = fields.Char(required=True)
    requestor_email = fields.Char()
    request_type = fields.Selection([
        ('access', 'Access'),
        ('erasure', 'Erasure'),
        ('rectification', 'Rectification'),
        ('portability', 'Portability'),
    ], required=True)
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
        vals.setdefault('name', 'DSR/%s' % (self.env['ir.sequence'].next_by_code('iso.dsr') if self.env.ref('iso27701', raise_if_not_found=False) else 'new'))
        if not vals.get('verification_token'):
            vals['verification_token'] = uuid.uuid4().hex
        rec = super().create(vals)
        rec.created_date = fields.Datetime.now()
        return rec

    def generate_verification_token(self):
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
        for rec in self:
            if rec.request_type in ('access', 'portability') and not rec.requestor_email:
                raise ValidationError('Requestor email is required for access and portability requests')

    def action_open(self):
        self.state = 'open'

    def action_done(self):
        self.state = 'done'

    def action_refuse(self):
        self.state = 'refused'

    def action_verify(self):
        """Mark request as verified by current user and open it for processing."""
        for rec in self:
            rec.verified_date = fields.Datetime.now()
            rec.verifier_id = self.env.uid
            rec.state = 'open'

