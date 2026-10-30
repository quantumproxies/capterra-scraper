# Capterra Scraper

[![ci](https://github.com/quantumproxies/capterra-scraper/actions/workflows/ci.yml/badge.svg)](https://github.com/quantumproxies/capterra-scraper/actions/workflows/ci.yml) ![python](https://img.shields.io/badge/python-3.9%2B-blue) ![license](https://img.shields.io/badge/license-MIT-green) ![dependencies](https://img.shields.io/badge/dependencies-none-brightgreen)

Scrape Capterra software categories from Python or the command line: every product listed in a category, with the vendor, overall star rating and its 1-to-5 breakdown, the ease-of-use, customer-service, features and value-for-money sub-scores, review counts by company size and period, starting price, free trial and free version flags, the feature list and whether the slot is a paid placement, as JSON or CSV. The code is free and open source (MIT). It runs on the QuanticData Data API, so there are no proxies to rotate and no headless browser to keep alive: sign in once and run a command.

```bash
pip install git+https://github.com/quantumproxies/capterra-scraper
capterra-scraper login
capterra-scraper products crm --max-results 50 -o crm_software.csv
```

`login` opens the QuanticData sign-in page in your browser. New accounts get $2 of free usage every month, no card required: [create one](https://app.quanticdata.io/register?utm_source=github&utm_medium=readme&utm_campaign=capterra-scraper).

## What it scrapes

| Command | Input | Returns | Per run |
|---|---|---|---|
| `capterra-scraper products` | software category | Name, vendor, rating, review counts, sub-scores, pricing, paid flag, 34 fields per row ([fields and price](https://quanticdata.io/collectors/capterra-scraper-api/?utm_source=github&utm_medium=readme&utm_campaign=capterra-scraper)) | up to 500 |

Capterra orders its category pages by bid, so the first rows are usually paid placements: `sponsored` and `bid_spot` (1 = top) tell an advertisement from an organic listing, and `rank` keeps Capterra's own order. `product_id` is the number in the product URL and stays stable, the key to deduplicate across categories.

## Sample output

A real row from `capterra-scraper products crm --max-results 3` (2026-10-23):

```json
{
  "url": "https://www.capterra.com/p/155928/Zoho-CRM/",
  "logo": "https://gdm-catalog-fmapi-prod.imgix.net/ProductLogo/82a342f4-1d08-4265-877a-83f0d7b3858f.png",
  "name": "Zoho CRM",
  "rank": 1,
  "slug": "Zoho-CRM",
  "rating": 4.31,
  "vendor": "Zoho",
  "reviews": 7007,
  "bid_spot": 1,
  "category": "CRM Software",
  "features": [
    "Activity Dashboard",
    "Activity Tracking",
    "AI Copilot",
    "Alerts/Notifications",
    "API",
    "Business Card/Badge Scanning",
    "Calendar Management",
    "Calendar/Reminder System"
  ],
  "sponsored": true,
  "product_id": 155928,
  "category_id": "4c7ba4f6-a5c3-4fcf-bb0b-388597ecee9d",
  "description": "Zoho CRM is an AI-powered sales CRM that empowers SMBs & enterprises of all sizes with a 360º customer relationship management solution",
  "ease_of_use": 4.15,
  "reviews_url": "https://www.capterra.com/p/155928/Zoho-CRM/reviews/",
  "product_uuid": "2143ac98-b65c-4bb1-ae6b-a6d200b7a22f",
  "functionality": 4.27,
  "pricing_plans": null,
  "has_free_trial": true,
  "price_currency": null,
  "starting_price": null,
  "value_for_money": 4.29,
  "customer_service": 4.08,
  "has_free_version": true,
  "long_description": "Zoho CRM empowers businesses of all sizes with a 360º customer relationship lifecycle management solution.",
  "rating_breakdown": {
    "1": 84,
    "2": 172,
    "3": 781,
    "4": 2388,
    "5": 3582
  },
  "reviews_mid_size": 581,
  "reviews_enterprise": 539,
  "reviews_last_6_months": 42,
  "reviews_last_12_months": 75,
  "reviews_small_business": 5286,
  "likelihood_to_recommend": 0.683
}
```

## Python

```python
from quanticdata_capterra_scraper import CapterraScraper

capterra = CapterraScraper()  # saved login, or QUANTICDATA_API_KEY

crm = capterra.products("crm", max_results=50)
for p in crm:
    print(p["rank"], p["sponsored"], p["name"], p["vendor"], p["rating"], p["reviews"])
crm.to_csv("crm_software.csv")

organic = [p for p in crm if not p["sponsored"]]
print(len(organic), "organic listings;", crm.rows[0]["rating_breakdown"])
```

Each call returns a `Run`: iterate it for the rows (plain dicts), take `len()`, or save it with `to_csv()`, `to_json()`, `to_jsonl()` or `to_dataframe()` (pandas). Errors are specific: `InsufficientCredit`, `RateLimited`, `InvalidInput`, `JobFailed`, `AuthError`.

## Examples

- **Several categories in one CSV**: List a few Capterra categories, deduplicate the products by Capterra id and keep the categories each one appears in, with vendor, ratings, sub-scores and pricing. See [`examples/categories_to_csv.py`](examples/categories_to_csv.py).
- **Organic ranking**: Drop the paid placements from a category and rank what is left by review count and rating, to see the order buyers would see without the ads. See [`examples/organic_ranking.py`](examples/organic_ranking.py).
- **Free versions worth trying**: Keep the products of a category that Capterra flags with a free version, above a minimum rating and review count, sorted by value-for-money score. See [`examples/free_versions.py`](examples/free_versions.py).

## Command line

Results print as a table; `-o file.csv`, `-o file.json` or `-o file.jsonl` writes a file. List inputs take `a b c`, `a,b,c`, `@file.txt` (one per line) or `-` (stdin). `--no-wait` starts a long run in the background and prints its id; `capterra-scraper run <id> -o out.csv` collects it later.

### `capterra-scraper products`

Software products from a Capterra category: vendor, rating, rating breakdown, sub-scores, pricing and paid-placement flag.

```
capterra-scraper products CATEGORY [options]
```

| Option | Type | Default | Description |
|---|---|---|---|
| `CATEGORY` | string |  | Software category as a plain keyword ("crm", "project management", "help desk", "accounting"), matched against Capterra's own category index, where an exact name wins ("crm" is CRM, not Construction CRM). A Capterra category slug or URL works too. |
| `--country` | string |  | Country to run the request from, as an ISO 3166-1 alpha-2 code (us, gb, de...). |
| `--max-results` | integer | `25` | How many products to deliver at most (1–500). You pay only for delivered products. |

## Output fields

<details><summary><code>capterra-scraper products</code>: 34 fields</summary>

| Field | Type | Description |
|---|---|---|
| `rank` | integer | Position in Capterra's own order for this response, counting across pages. Note this order is bid-driven, not merit-driven — see `sponsored`. |
| `product_id` | integer | Capterra's numeric product id (its `seoId`, the number in the product URL). Stable, and the key used to de-duplicate. |
| `product_uuid` | string or null | Capterra's internal product UUID. |
| `name` | string | Product name. |
| `vendor` | string or null | Company behind the product, e.g. "Oracle" for NetSuite. Published in Capterra's data layer only — it does not appear anywhere in the rendered listing card. |
| `rating` | number or null | Overall star rating out of 5, rounded to 2 decimals. Capterra publishes it at raw float precision (4.233430091920658) and prints it as 4.2. |
| `reviews` | integer or null | Total number of reviews. 1 is a real value and is kept — several listed products have a single 5.0 review. |
| `rating_breakdown` | object or null | Star histogram as {"1":n,…,"5":n}, keyed by star value. Capterra emits these buckets unordered and omits a star nobody awarded. |
| `ease_of_use` | number or null | Capterra's "Ease of Use" sub-score out of 5, rounded to 2 decimals. |
| `customer_service` | number or null | Capterra's "Customer Service" sub-score out of 5, rounded to 2 decimals. |
| `functionality` | number or null | Capterra's "Features" / functionality sub-score out of 5, rounded to 2 decimals. |
| `value_for_money` | number or null | Capterra's "Value for Money" sub-score out of 5, rounded to 2 decimals. |
| `likelihood_to_recommend` | number or null | Likelihood to recommend as the 0–1 fraction Capterra publishes (0.63 = the 63% its UI shows). |
| `description` | string or null | The short product description Capterra shows on the listing card. |
| `category` | string or null | The category being listed, e.g. "CRM Software", read from the page breadcrumb. |
| `category_id` | string or null | Capterra's internal UUID for the category. |
| `starting_price` | number or null | Starting price of the default plan, in price_currency, when Capterra publishes a pricing plan for the product. |
| `price_currency` | string or null | Currency of starting_price. |
| `pricing_plans` | integer or null | How many pricing plans Capterra lists for the product. Null when it publishes none. |
| `has_free_trial` | boolean or null | Whether Capterra flags a free trial. |
| `has_free_version` | boolean or null | Whether Capterra flags a free version. |
| `sponsored` | boolean | True when the row is a paid placement. Capterra orders its directories by bid, so this is how to tell an advertisement from an organic listing. |
| `bid_spot` | integer or null | The advertising slot the vendor paid for (1 = top). Null on organic rows. |
| `logo` | string or null | Product logo image URL. |
| `slug` | string or null | Capterra's URL slug for the product. |
| `url` | string or null | Capterra product page URL. |
| `reviews_url` | string or null | Capterra reviews page URL, only when the product actually publishes one. |
| `long_description` | string or null | The product's full description, when the listing carries one. |
| `features` | string[] or null | Feature names Capterra lists for the product, alphabetical — the category listing carries at most the first 50. |
| `reviews_small_business` | integer or null | Reviews written by small businesses. |
| `reviews_mid_size` | integer or null | Reviews written by mid-size businesses. |
| `reviews_enterprise` | integer or null | Reviews written by enterprises. |
| `reviews_last_6_months` | integer or null | Reviews published in the last 6 months. |
| `reviews_last_12_months` | integer or null | Reviews published in the last 12 months. |

</details>

## Sign-in and API keys

- `capterra-scraper login` signs you in with OAuth 2.1 and PKCE in the browser. The token is stored in `~/.config/quanticdata/credentials.json` (readable only by you) and refreshed automatically. One login serves every QuanticData tool on the machine.
- No browser on the machine (SSH, Docker, Colab): run `capterra-scraper login --no-browser`, open the link anywhere, then paste back the address the browser ends on.
- Scripts and CI: set `QUANTICDATA_API_KEY` to a key from the dashboard, or store one with `capterra-scraper login --api-key`.
- `capterra-scraper logout` revokes the token. The connection is listed under API keys in the dashboard as "API · QuanticData CLI"; deleting that key disconnects every machine that uses it.

## Pricing

The code is free and MIT-licensed. Runs are billed to your QuanticData account per delivered row, at the price shown on each collector page linked above; $2 of usage is free every month and failed runs are never billed. Plans with higher limits: [pricing](https://quanticdata.io/pricing/?utm_source=github&utm_medium=readme&utm_campaign=capterra-scraper).

## Other ways to call it

The same data over plain HTTP:

```bash
curl -X POST https://api.quanticdata.io/v1/scraper/collectors/capterra_products/run \
  -H "Authorization: Bearer $QUANTICDATA_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"input": {"category": "crm", "max_results": 3}}'
```

- [API reference](https://quanticdata.io/docs/?utm_source=github&utm_medium=readme&utm_campaign=capterra-scraper) with Python, Node, PHP and curl examples.
- [MCP server](https://quanticdata.io/mcp-server/?utm_source=github&utm_medium=readme&utm_campaign=capterra-scraper) to give Claude, Cursor or any MCP client the same tools.
- [n8n node](https://github.com/quantumproxies/n8n-nodes-quanticdata) for no-code workflows.

## FAQ

**Is this Capterra scraper free?**

The code is free and MIT-licensed. Scraping runs on your QuanticData account: $2 of usage is free every month with no card, then you pay per delivered row at the price shown on each collector page. Failed runs are never billed.

**Do I need proxies or a headless browser?**

No. You send a category and get rows back; the requests run on QuanticData's side.

**What does each row contain?**

One product of the category: vendor, overall rating and star histogram, four sub-scores, likelihood to recommend, review counts (total, by company size, last 6 and 12 months), starting price and number of plans, free trial and free version flags, feature list, descriptions and links.

**How many products can one run return?**

Up to 500 products per run; ask for fewer with --max-results and you pay only for what is delivered.

**Can I export to CSV or Excel?**

Add -o results.csv (or .json, .jsonl). The rating breakdown becomes rating_breakdown.1 to rating_breakdown.5 and the feature list is joined with '; ', so the CSV opens cleanly in Excel or Google Sheets.

**Can I run it on a schedule?**

Yes. Set QUANTICDATA_API_KEY in the environment and call the CLI or examples/categories_to_csv.py from cron, GitHub Actions or any scheduler.

## Related scrapers

- [G2 Scraper](https://github.com/quantumproxies/g2-scraper): G2 scraper for Python and the command line.
- [Website Technology Checker](https://github.com/quantumproxies/website-technology-checker): Website technology checker for Python and the command line.
- [Company Data API](https://github.com/quantumproxies/company-data-api): Company data API for Python and the command line.

## License

MIT. Built and maintained by [QuanticData](https://quanticdata.io/?utm_source=github&utm_medium=readme&utm_campaign=capterra-scraper).
