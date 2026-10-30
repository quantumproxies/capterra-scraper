"""Row types of each command, for editors and type checkers (rows are plain dicts)."""

from typing import Any, Dict, List, Optional

try:  # Python 3.8+
    from typing import TypedDict
except ImportError:  # pragma: no cover
    from typing_extensions import TypedDict  # type: ignore


class CapterraProductsRow(TypedDict, total=False):
    """One row of `capterra-scraper products` (capterra_products v1.1.1)."""

    rank: int
    """Position in Capterra's own order for this response, counting across pages. Note this order is bid-driven, not merit-driven — see `sponsored`."""
    product_id: int
    """Capterra's numeric product id (its `seoId`, the number in the product URL). Stable, and the key used to de-duplicate."""
    product_uuid: Optional[str]
    """Capterra's internal product UUID."""
    name: str
    """Product name."""
    vendor: Optional[str]
    """Company behind the product, e.g. "Oracle" for NetSuite. Published in Capterra's data layer only — it does not appear anywhere in the rendered listing card."""
    rating: Optional[float]
    """Overall star rating out of 5, rounded to 2 decimals. Capterra publishes it at raw float precision (4.233430091920658) and prints it as 4.2."""
    reviews: Optional[int]
    """Total number of reviews. 1 is a real value and is kept — several listed products have a single 5.0 review."""
    rating_breakdown: Dict[str, Any]
    """Star histogram as {"1":n,…,"5":n}, keyed by star value. Capterra emits these buckets unordered and omits a star nobody awarded."""
    ease_of_use: Optional[float]
    """Capterra's "Ease of Use" sub-score out of 5, rounded to 2 decimals."""
    customer_service: Optional[float]
    """Capterra's "Customer Service" sub-score out of 5, rounded to 2 decimals."""
    functionality: Optional[float]
    """Capterra's "Features" / functionality sub-score out of 5, rounded to 2 decimals."""
    value_for_money: Optional[float]
    """Capterra's "Value for Money" sub-score out of 5, rounded to 2 decimals."""
    likelihood_to_recommend: Optional[float]
    """Likelihood to recommend as the 0–1 fraction Capterra publishes (0.63 = the 63% its UI shows)."""
    description: Optional[str]
    """The short product description Capterra shows on the listing card."""
    category: Optional[str]
    """The category being listed, e.g. "CRM Software", read from the page breadcrumb."""
    category_id: Optional[str]
    """Capterra's internal UUID for the category."""
    starting_price: Optional[float]
    """Starting price of the default plan, in price_currency, when Capterra publishes a pricing plan for the product."""
    price_currency: Optional[str]
    """Currency of starting_price."""
    pricing_plans: Optional[int]
    """How many pricing plans Capterra lists for the product. Null when it publishes none."""
    has_free_trial: Optional[bool]
    """Whether Capterra flags a free trial."""
    has_free_version: Optional[bool]
    """Whether Capterra flags a free version."""
    sponsored: bool
    """True when the row is a paid placement. Capterra orders its directories by bid, so this is how to tell an advertisement from an organic listing."""
    bid_spot: Optional[int]
    """The advertising slot the vendor paid for (1 = top). Null on organic rows."""
    logo: Optional[str]
    """Product logo image URL."""
    slug: Optional[str]
    """Capterra's URL slug for the product."""
    url: Optional[str]
    """Capterra product page URL."""
    reviews_url: Optional[str]
    """Capterra reviews page URL, only when the product actually publishes one."""
    long_description: Optional[str]
    """The product's full description, when the listing carries one."""
    features: Optional[List[str]]
    """Feature names Capterra lists for the product, alphabetical — the category listing carries at most the first 50."""
    reviews_small_business: Optional[int]
    """Reviews written by small businesses."""
    reviews_mid_size: Optional[int]
    """Reviews written by mid-size businesses."""
    reviews_enterprise: Optional[int]
    """Reviews written by enterprises."""
    reviews_last_6_months: Optional[int]
    """Reviews published in the last 6 months."""
    reviews_last_12_months: Optional[int]
    """Reviews published in the last 12 months."""
