from odoo import http
from odoo.http import request, content_disposition
import os

from ..utils.mapping_helpers import convert_md_to_csv


class Iso27701Controller(http.Controller):
    @http.route('/iso27701/mapping.csv', type='http', auth='user', methods=['GET'], csrf=False)
    def mapping_csv(self, **kwargs):
        """Serve the ISO27701 mapping markdown as a CSV download.

        Note: this controller runs only inside an Odoo runtime where the addon
        is installed. It reads `data/iso27701_mapping.md` from the addon folder.
        """
        module_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
        md_path = os.path.join(module_dir, 'data', 'iso27701_mapping.md')
        # Restrict endpoint to staff/admin users only
        user = request.env.user
        try:
            is_admin = user.has_group('base.group_system')
            is_staff = user.has_group('base.group_user')
        except Exception:
            is_admin = False
            is_staff = False
        if not (is_admin or is_staff):
            return request.make_response('Forbidden', [('Content-Type', 'text/plain')], status=403)

        if not os.path.exists(md_path):
            return request.not_found()
        try:
            with open(md_path, 'r', encoding='utf-8') as fh:
                md = fh.read()
            csv_text = convert_md_to_csv(md)
            headers = [
                ('Content-Type', 'text/csv; charset=utf-8'),
                ('Content-Disposition', content_disposition('iso27701_mapping.csv')),
            ]
            return request.make_response(csv_text, headers)
        except Exception as e:
            return request.make_response(str(e), [('Content-Type', 'text/plain')], status=500)
