# Dataset v3 (Full Schema, Realistic Messy Data) Statistics

- Total rows: **18,490**
- Clean base rows: **16,000**
- Exact duplicates added: **420**
- Cancelled rows added: **630**
- Messy rows injected: **1,440**

## Schema

| Column | Included |
|---|---|
| `sale_id` | Yes |
| `sale_type` | Yes |
| `sales_channel` | Yes |
| `product_name` | Yes |
| `product_category` | Yes |
| `product_brand` | Yes |
| `customer_name` | Yes |
| `customer_email` | Yes |
| `customer_country` | Yes |
| `customer_city` | Yes |
| `customer_gender` | Yes |
| `customer_segment` | Yes |
| `quantity` | Yes |
| `unit_price` | Yes |
| `cost_price` | Yes |
| `discount` | Yes |
| `store_location` | Yes |
| `store_region` | Yes |
| `store_manager` | Yes |
| `sale_date` | Yes |
| `order_timestamp` | Yes |
| `delivery_date` | Yes |
| `order_status` | Yes |

## Customer and Product Coverage

- Unique customer emails: **499**
- Unique customer names: **499**
- Unique products: **11**

## Guaranteed Messy Cases

| Issue Type | Intended Rows |
|---|---:|
| `missing_sale_type` | 70 |
| `missing_sales_channel` | 70 |
| `missing_product_name` | 80 |
| `missing_customer_email` | 80 |
| `invalid_customer_email` | 80 |
| `invalid_quantity` | 80 |
| `invalid_unit_price` | 80 |
| `invalid_discount_string` | 80 |
| `missing_store_location` | 80 |
| `invalid_store_location` | 80 |
| `missing_sale_date` | 80 |
| `invalid_sale_date` | 80 |
| `invalid_sale_id_non_integer` | 80 |
| `missing_customer_name` | 80 |
| `multi_error_rows` | 120 |
| `format_noise_rows` | 220 |

## Quick Data Quality Checks

| Metric | Count |
|---|---:|
| Missing `sale_id` | 630 |
| Missing `sale_type` | 100 |
| Missing `sales_channel` | 70 |
| Missing `product_name` | 110 |
| Missing `customer_name` | 110 |
| Missing `customer_email` | 110 |
| Missing `store_location` | 80 |
| Missing `sale_date` | 80 |
| Invalid email format | 80 |
| Invalid store location | 110 |
| Invalid date format (obvious injected) | 110 |

## Notes

- `customer_name` is included and uses realistic full names like `John Smith` and `Jane Taylor`.
- The dataset contains both valid and messy rows across the **full intended schema**.
- Messiness includes nulls, invalid formats, conflicting field values, whitespace noise, and casing variation.
- This dataset is intended for **Bronze → Silver → Gold** teaching and data quality analysis.