import csv
import io
from typing import List, Tuple


def parse_mapping_md(md_text: str) -> List[Tuple[str, str, str]]:
    """Parse a simple markdown table of ISO mapping into rows.

    Expects a table like:
    | ISO 27701 Control | Description | Repository Feature / Status |
    |---|---|---|
    | 7.4.1 Logging | Maintain logs | auditlog module |

    Returns list of (control, description, feature).
    """
    # Rows are represented as:
    # (iso_control, description, repository_feature_or_status)
    rows = []
    lines = [l.strip() for l in md_text.splitlines()]

    # Find the markdown header separator, for example:
    # |---|---|---|
    # or variants containing spaces/colons for alignment.
    for i, ln in enumerate(lines):
        if ln.startswith('|') and set(ln.replace('|', '').strip()) <= set('- :'):
            header_idx = i - 1
            break
    else:
        # No markdown table found -> return empty rows instead of failing.
        return rows

    # Collect table body starting after header + separator lines.
    for ln in lines[header_idx+2:]:
        # Stop parsing on first non-table line.
        if not ln.startswith('|'):
            break
        # Split by pipe and drop first/last empty cells caused by edge pipes.
        parts = [p.strip() for p in ln.split('|')[1:-1]]
        if len(parts) >= 3:
            rows.append((parts[0], parts[1], parts[2]))
    return rows


def mapping_rows_to_csv(rows: List[Tuple[str, str, str]]) -> str:
    """Serialize mapping rows into CSV text with a deterministic header.

    The output is UTF-8 compatible plain text and can be returned directly
    from Odoo HTTP responses.
    """
    out = io.StringIO()
    writer = csv.writer(out)
    # Keep header names auditor-friendly and stable for automation.
    writer.writerow(['ISO Control', 'Description', 'Repository Feature / Status'])
    for r in rows:
        writer.writerow(list(r))
    return out.getvalue()


def convert_md_to_csv(md_text: str) -> str:
    """Convenience adapter: markdown table text -> CSV text."""
    rows = parse_mapping_md(md_text)
    return mapping_rows_to_csv(rows)
