"""Several Capterra software categories in one CSV, one row per product.

    python categories_to_csv.py crm "help desk" "project management" --per-category 100

Products are deduplicated by Capterra product id; each keeps the categories
it was listed in. The CSV has vendor, rating, review count, the four
sub-scores, starting price, free trial and free version flags, and whether
the product appeared as a paid placement in any category.
"""

import argparse

from quanticdata_capterra_scraper import CapterraScraper, write

FIELDS = ["name", "vendor", "categories", "rating", "reviews", "ease_of_use", "customer_service", "functionality",
          "value_for_money", "likelihood_to_recommend", "starting_price", "price_currency", "has_free_trial",
          "has_free_version", "sponsored_anywhere", "product_id", "url"]


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("categories", nargs="+", help='plain keywords, e.g. crm "help desk"')
    parser.add_argument("--per-category", type=int, default=100, help="products per category (max 500)")
    parser.add_argument("--out", default="capterra_products.csv")
    args = parser.parse_args()

    capterra = CapterraScraper()
    products = {}
    for category in args.categories:
        run = capterra.products(category, max_results=args.per_category)
        for p in run:
            entry = products.setdefault(p["product_id"], {**p, "categories": [], "sponsored_anywhere": False})
            entry["categories"].append(p.get("category") or category)
            entry["sponsored_anywhere"] = entry["sponsored_anywhere"] or bool(p.get("sponsored"))
        label = run.rows[0].get("category") if len(run) else category
        print(f"{category!r} ({label}): {len(run)} products")

    rows = [{k: p.get(k) for k in FIELDS} for p in products.values()]
    write(rows, args.out)
    print(f"{len(rows)} unique products written to {args.out}")


if __name__ == "__main__":
    main()
