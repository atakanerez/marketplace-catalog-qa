# Marketplace Catalog QA

A Python command-line tool that catches catalog feed errors before a bulk product upload. It reads CSV locally and returns JSON issues with row numbers, field names, and reasons. It uses synthetic data and requires no packages or marketplace credentials.

## Run

Use Python 3.10+.

```sh
python validate_catalog.py sample_catalog.csv
```

The demo includes five issues: a duplicate SKU, a repeated variant within its product group, an invalid price, negative stock, and a missing title. Correct them and rerun to get an empty JSON array.

| Column | Rule |
| --- | --- |
| `sku` | Required and unique, ignoring case |
| `product_group`, `variant` | Both required; the pair must be unique, ignoring case |
| `title` | Required |
| `price` | Positive, finite decimal with a dot separator |
| `stock` | Whole number, zero or above |

Exit codes: **0** clean; **1** validation issues; **2** input or read error. This is a generic validation example; each marketplace can add its own required columns or category rules.
