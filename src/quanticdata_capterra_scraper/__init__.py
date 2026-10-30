"""Capterra Scraper: Capterra scraper for Python and the command line: the software products of a Capterra category with vendor, star rating, rating breakdown, sub-scores, review counts, starting price, free trial and paid-placement flag, as JSON or CSV. Free and open source; sign in with your QuanticData account, no proxies or headless browser to run.

    from quanticdata_capterra_scraper import CapterraScraper

    scraper = CapterraScraper()   # saved login (`capterra-scraper login`) or QUANTICDATA_API_KEY
    run = scraper.products(...)   # software products listed in a Capterra category
"""

from typing import Any, Dict, Optional, Sequence, Union

from ._qd.client import Client, Run
from ._qd.errors import (APIError, AuthError, InsufficientCredit, InvalidInput, JobFailed, JobTimeout,
                         QuanticDataError, RateLimited)
from ._qd.output import write

__version__ = "0.1.0"
__all__ = ["CapterraScraper", "Run", "write", "APIError", "AuthError", "InsufficientCredit", "InvalidInput",
           "JobFailed", "JobTimeout", "QuanticDataError", "RateLimited", "__version__"]


def _as_list(value: Any) -> Any:
    if value is None or isinstance(value, (list, tuple)):
        return list(value) if value is not None else None
    return [value]


class CapterraScraper:
    """Capterra Scraper on the QuanticData Data API.

    Every method runs one collector and returns a :class:`Run`: iterate it for the
    rows (plain dicts, typed in ``types``), or save it with ``to_csv()``,
    ``to_json()``, ``to_jsonl()`` or ``to_dataframe()``.
    """

    def __init__(self, api_key: Optional[str] = None, *, timeout: float = 180.0) -> None:
        self.client = Client(api_key, user_agent="capterra-scraper/0.1.0 (+https://github.com/quantumproxies/capterra-scraper)", timeout=timeout)

    def products(
        self, category: str,
        *,
        country: Optional[str] = None,
        max_results: Optional[int] = None,
        wait: bool = True,
        timeout: float = 900.0,
    ) -> Run:
        """Software products from a Capterra category: vendor, rating, rating breakdown, sub-scores, pricing and paid-placement flag.

        Args:
            category: Software category as a plain keyword ("crm", "project management", "help desk", "accounting"), matched against Capterra's own category index, where an exact name wins ("crm" is CRM, not Construction CRM). A Capterra category slug or URL works too.
            country: Country to run the request from, as an ISO 3166-1 alpha-2 code (us, gb, de...).
            max_results: How many products to deliver at most (1–500). You pay only for delivered products.
            wait: False starts the run in the background and returns its id at once.
            timeout: seconds to wait for a background run before giving up.

        Returns up to 500 rows, one per product: see ``types.CapterraProductsRow``.
        """
        payload = {
            "category": category,
            "country": country,
            "max_results": max_results,
        }
        return self.client.run_collector("capterra_products", payload, wait=wait, timeout=timeout)
