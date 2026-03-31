from odoo import http
from odoo.http import request, content_disposition
import os

from ..utils.mapping_helpers import convert_md_to_csv


class Iso27701Controller(http.Controller):
    # Public endpoint for downloading the ISO control-to-feature mapping as CSV.
    #
    # Why `auth='user'`:
    # - We only allow authenticated users to access this route.
    # - Additional group checks below further limit to staff/admin roles.
    @http.route('/iso27701/mapping.csv', type='http', auth='user', methods=['GET'], csrf=False)
    def mapping_csv(self, **kwargs):
        """Serve the ISO27701 mapping markdown as a CSV download.

        Note: this controller runs only inside an Odoo runtime where the addon
        is installed. It reads `data/iso27701_mapping.md` from the addon folder.
        """
        # Resolve addon-local file path so this works in any deployment layout
        # (local dev, Docker container, or packaged addon installation).
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

        # Return 404 when mapping source file is missing from addon data.
        if not os.path.exists(md_path):
            return request.not_found()
        try:
            # Read markdown mapping and convert it in-memory to CSV text.
            with open(md_path, 'r', encoding='utf-8') as fh:
                md = fh.read()
            csv_text = convert_md_to_csv(md)
            headers = [
                ('Content-Type', 'text/csv; charset=utf-8'),
                # Force browser download with a stable filename.
                ('Content-Disposition', content_disposition('iso27701_mapping.csv')),
            ]
            return request.make_response(csv_text, headers)
        except Exception as e:
            # Keep failure explicit for easier troubleshooting in demos/dev.
            return request.make_response(str(e), [('Content-Type', 'text/plain')], status=500)
