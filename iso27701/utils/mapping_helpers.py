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
    rows = []
    lines = [l.strip() for l in md_text.splitlines()]
    # find header separator
    for i, ln in enumerate(lines):
        if ln.startswith('|') and set(ln.replace('|', '').strip()) <= set('- :'):
            header_idx = i - 1
            break
    else:
        return rows

    # collect table body starting at header_idx+2
    for ln in lines[header_idx+2:]:
        if not ln.startswith('|'):
            break
        parts = [p.strip() for p in ln.split('|')[1:-1]]
        if len(parts) >= 3:
            rows.append((parts[0], parts[1], parts[2]))
    return rows


def mapping_rows_to_csv(rows: List[Tuple[str, str, str]]) -> str:
    out = io.StringIO()
    writer = csv.writer(out)
    writer.writerow(['ISO Control', 'Description', 'Repository Feature / Status'])
    for r in rows:
        writer.writerow(list(r))
    return out.getvalue()


def convert_md_to_csv(md_text: str) -> str:
    rows = parse_mapping_md(md_text)
    return mapping_rows_to_csv(rows)
