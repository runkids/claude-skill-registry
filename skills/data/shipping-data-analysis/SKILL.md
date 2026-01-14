---
name: shipping-data-analysis
description: |
  Shipping Data Analysis - Brock's Reusable Prompt v4.0
  Analyzes any shipping dataset with FirstMile-branded deliverables, normalized address grouping,
  and conditional advanced analytics based on available data fields.

  Use when:
  (1) Prospect provides shipping data (PLD, exports, etc.)
  (2) "analyze shipping data" or "shipping analysis"
  (3) "run Brock's prompt" or "data analysis v4.0"
  (4) Need DIM exposure, zone distribution, or cost intelligence reports
  (5) Creating prospect-facing shipping profile analysis

  Triggers on: "shipping analysis", "analyze shipping", "PLD analysis", "Brock's prompt",
               "data analysis v4.0", "shipping profile", "DIM exposure", "zone distribution"
---

# Shipping Data Analysis Skill

> *Brock Hansen's Reusable Prompt v4.0 - FirstMile branded shipping analytics*

## Overview

This skill generates comprehensive shipping analysis workbooks using Brock's standardized v4.0 prompt structure. It produces up to 16 Excel sheets with FirstMile branding, intelligent address normalization, and conditional advanced analytics.

## Quick Start

```
/shipping-analysis [file.xlsx] --company "Company Name"
```

## Required Inputs

| Input | Description |
|-------|-------------|
| **File** | Excel/CSV with shipping data |
| **Company Name** | Used in all report titles |
| **Column Mapping** | Map your columns to standard fields |

## Column Mapping (Required)

| Field | Your Column | Notes |
|-------|-------------|-------|
| Order Date | _____ | "Order Date", "Ship Date", "Label Created Date" |
| Ship Address (Origin) | _____ | Warehouse/fulfillment center |
| Service Level | _____ | Carrier service name |
| Tracking Number | _____ | For carrier inference |
| Weight | _____ | Specify oz or lbs |
| Dimensions | _____ | L/W/H or DIMS Grouped |

## Optional Columns (Enable Advanced Modules)

| Field | Enables |
|-------|---------|
| Delivered Date | Transit time & on-time analysis |
| Destination ZIP/State | Zone distribution & lane analysis |
| Zone | Zone distribution sheet |
| Total Charge/Cost | Cost intelligence module |
| Surcharges | Surcharge mix analysis |
| L/W/H Dimensions | DIM exposure analysis |

## Output Structure

### Core Sheets (Always Generated)

| # | Sheet | Content |
|---|-------|---------|
| 1 | Executive Summary | Top 10 Origins, Weight Bands, Monthly Volume |
| 2 | Monthly Shipments | Monthly breakdown with percentages |
| 3 | Bill Weight Distribution | Weight sorted ascending |
| 4 | DIMS Grouped Distribution | Dimension combos by count |
| 5 | Ship Address Distribution | Normalized addresses |
| 6 | Service Level Distribution | Carrier x Service matrix |

### Conditional Sheets (If Data Exists)

| # | Sheet | Requires |
|---|-------|----------|
| 7 | Zone Distribution | Zone column |
| 8 | Destination Footprint | Dest State/ZIP |
| 9 | Transit Time Analysis | Delivered Date + Ship Date |
| 10 | Cost Intelligence | Total Charge/Cost |
| 11 | Surcharge Analysis | Surcharge columns |
| 12 | DIM Exposure Analysis | L/W/H + Scale Weight |
| 13 | Service Level Mismatch | Delivered Date |
| 14 | Operational Trends | 4+ weeks data |
| 15 | Data Quality & Exceptions | All fields (checks missing) |
| 16 | Claims/Exception Exposure | Exception Code/Status |

## FirstMile Branding

| Element | Style |
|---------|-------|
| Headers | Navy #192F66, white text, bold |
| Column Headers | Light green #B0D67B, black, bold |
| Alternating Rows | Beige #FAF9F5 / white |
| Green accent | #4DA519 |

## Key Features

### Address Normalization
Combines address variations like a pivot table:
- "300 Seabrook Parkway" + "300 SEABROOK PKWY" → Same warehouse
- Uppercase, standardize abbreviations (ST, AVE, BLVD)
- Reduces unique addresses by ~10-15%

### DIM Exposure Analysis
- Standard DIM divisor: 139 (166 for USPS)
- Calculates: `dim_weight = (L x W x H) / 139 * 16`
- Identifies right-size opportunities

### Carrier Inference
From tracking number patterns:
- 9400, 9205, 9208, 9261 → USPS
- 12-15 digit numeric → FedEx
- Starts with "1Z" → UPS

## Usage Examples

### Example 1: Full Analysis
```
File: Acme_Shipping_Q4.xlsx
Company: Acme Distribution

Column Mapping:
- Order Date: Column B
- Ship Address: Column G
- Service Level: Column K
- Tracking: Column AB
- Weight (oz): Column R
- Delivered Date: Column AD
- Zone: Column M
- Total Charge: Column AE

Run full analysis with all advanced modules.
```

### Example 2: Basic Analysis (Limited Data)
```
File: Client_Export.xlsx
Company: Beta Brands

Column Mapping:
- Order Date: Column B
- Ship Address: Column G
- Service Level: Column K
- Weight (oz): Column R
- DIMS: L(S), W(T), H(U)

No cost or delivery data. Run core + DIM exposure.
```

## Workflow

1. **Upload file** and provide company name
2. **Map columns** to standard fields
3. **Identify optional columns** for advanced modules
4. **Generate analysis** - produces branded Excel workbook
5. **Review insights** - text summary of findings

## Reference Files

- `references/full-prompt.md` - Complete v4.0 prompt text
- `references/column-mapping.md` - Detailed field mapping guide
- `references/output-tables.md` - All table structures

---

*Source: Brock Hansen, VP of Sales - "Prompt for Quick Data Analysis" (Dec 17, 2025)*
