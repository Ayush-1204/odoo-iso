"""iso27701 package init for Python imports and tests.

This file avoids importing the `models` subpackage at import-time so that
pure-Python tests (which import `iso27701.utils`) do not require Odoo to be
installed. Odoo will import the `models` package when the addon is loaded in
an Odoo runtime.
"""

__all__ = []
