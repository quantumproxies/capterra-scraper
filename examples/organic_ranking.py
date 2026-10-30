"""A Capterra category without the paid placements, ranked by reviews and rating.

    python organic_ranking.py "project management" --max 200 --min-reviews 50

Capterra orders its category pages by bid. This keeps the organic listings
(sponsored = false), ranks them by review count and then rating, prints the
top 20 next to their position in Capterra's own order and writes the full
list to organic.csv.
"""

import argparse

from quanticdata_capterra_scraper import CapterraScraper, write


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("category")
    parser.add_argument("--max", type=int, default=200, help="products to read (max 500)")
    parser.add_argument("--min-reviews", type=int, default=10)
    parser.add_argument("--out", default="organic.csv")
    args = parser.parse_args()

    capterra = CapterraScraper()
    run = capterra.products(args.category, max_results=args.max)
    organic = [p for p in run if not p.get("sponsored") and (p.get("reviews") or 0) >= args.min_reviews]
    organic.sort(key=lambda p: (-(p.get("reviews") or 0), -(p.get("rating") or 0)))

    paid = sum(1 for p in run if p.get("sponsored"))
    print(f"{len(run)} products read, {paid} paid placements left out")
    print(f"{'#':>3} {'capterra':>8}  {'reviews':>7} {'rating':>6}  name")
    for i, p in enumerate(organic[:20], 1):
        print(f"{i:3d} {p['rank']:8d}  {p.get('reviews') or 0:7d} {p.get('rating') or 0:6.2f}  {p['name']} ({p.get('vendor') or '-'})")

    write([{"organic_rank": i, **p} for i, p in enumerate(organic, 1)], args.out)
    print(f"{len(organic)} organic products written to {args.out}")


if __name__ == "__main__":
    main()
