from typing import Optional, Dict


ADEQUATE_COUNTRIES = {
    'AT','BE','BG','HR','CY','CZ','DK','EE','FI','FR','DE','GR','HU','IE','IT','LV','LT','LU','MT','NL','PL','PT','RO','SK','SI','ES','SE',
    'UK','US','CA','AU','JP'
}


def create_processor(name: str, contact: Optional[str] = None, contract_reference: Optional[str] = None,
                     country: Optional[str] = None, data_types: Optional[str] = None) -> Dict:
    """Create a lightweight processor record (dict) for tests.

    `country` should be a country code or name; matching is case-insensitive.
    """
    return {
        'name': name,
        'contact': contact,
        'contract_reference': contract_reference,
        'country': country,
        'data_types': data_types,
    }


def is_high_risk_transfer(country: Optional[str]) -> bool:
    """Return True if transfers to `country` are likely high-risk (no adequacy).

    This is a heuristic used in tests; real assessments require legal review.
    """
    if not country:
        return True
    code = country.strip().upper()
    return code not in ADEQUATE_COUNTRIES


def summarize_processor(proc: Dict) -> str:
    parts = [proc.get('name') or 'Unnamed']
    if proc.get('country'):
        parts.append(f"({proc.get('country')})")
    if proc.get('contract_reference'):
        parts.append(f"contract={proc.get('contract_reference')}")
    return ' '.join(parts)
