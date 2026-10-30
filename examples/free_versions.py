"""Products of a Capterra category with a free version, sorted by value for money.

    python free_versions.py accounting --min-rating 4.3 --min-reviews 100

Keeps the products Capterra flags with a free version (has_free_version),
at or above a minimum rating and review count, and writes them to
free_versions.csv sorted by the value-for-money sub-score, with ease of use,
customer service, features and the free trial flag alongside.
"""

import argparse

from quanticdata_capterra_scraper import CapterraScraper, write

FIELDS = ["name", "vendor", "rating", "reviews", "value_for_money", "ease_of_use", "customer_service",
          "functionality", "has_free_trial", "starting_price", "price_currency", "url"]


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("category")
    parser.add_argument("--min-rating", type=float, default=4.0)
    parser.add_argument("--min-reviews", type=int, default=20)
    parser.add_argument("--max", type=int, default=300, help="products to read (max 500)")
    parser.add_argument("--out", default="free_versions.csv")
    args = parser.parse_args()

    capterra = CapterraScraper()
    run = capterra.products(args.category, max_results=args.max)
    free = [p for p in run if p.get("has_free_version")
            and (p.get("rating") or 0) >= args.min_rating and (p.get("reviews") or 0) >= args.min_reviews]
    free.sort(key=lambda p: -(p.get("value_for_money") or 0))

    write([{k: p.get(k) for k in FIELDS} for p in free], args.out)
    print(f"{len(free)} of {len(run)} products have a free version and pass the filters, written to {args.out}")
    for p in free[:10]:
        print(f"  {p.get('value_for_money') or 0:.2f}  {p['name']}  ({p.get('rating')}, {p.get('reviews')} reviews)")


if __name__ == "__main__":
    main()
