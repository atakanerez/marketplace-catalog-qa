"""Validate a marketplace product feed without uploading it."""
import argparse
import csv
import json
from decimal import Decimal, InvalidOperation
from pathlib import Path

FIELDS = ("sku", "product_group", "variant", "title", "price", "stock")

def validate(path):
    issues, skus, variants = [], set(), set()
    with path.open(encoding="utf-8-sig", newline="") as handle:
        rows = csv.DictReader(handle)
        missing = sorted(set(FIELDS) - set(rows.fieldnames or []))
        if missing:
            return [{"row": 1, "field": "header", "issue": "missing: " + ", ".join(missing)}]
        for row in rows:
            line = rows.line_num
            def add(field, issue):
                issues.append({"row": line, "field": field, "issue": issue})
            sku, group, variant, title, price, stock = (
                (row[name] or "").strip() for name in FIELDS
            )
            for name, value in zip(FIELDS[:4], (sku, group, variant, title)):
                if not value:
                    add(name, "required")
            key = sku.casefold()
            if key:
                if key in skus:
                    add("sku", "duplicate")
                skus.add(key)
            pair = (group.casefold(), variant.casefold())
            if all(pair):
                if pair in variants:
                    add("variant", "duplicate in product group")
                variants.add(pair)
            try:
                value = Decimal(price)
                if not value.is_finite() or value <= 0:
                    raise InvalidOperation
            except InvalidOperation:
                add("price", "expected a positive decimal")
            if not (stock.isascii() and stock.isdecimal()):
                add("stock", "expected a non-negative integer")
    return issues

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("feed", type=Path)
    args = parser.parse_args()
    try:
        issues = validate(args.feed)
    except (OSError, UnicodeError, csv.Error) as exc:
        parser.exit(2, f"Could not read feed: {exc}\n")
    print(json.dumps(issues, ensure_ascii=False, indent=2))
    return int(bool(issues))

if __name__ == "__main__":
    raise SystemExit(main())
