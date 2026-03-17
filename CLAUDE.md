# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Context

This is a **take-home analytics engineering hiring exercise** for Uber's Growth Strategy & Planning (GS&P) team. The goal is to help NYC Operations prioritize food delivery expansion by postal code.

## Data

**`internal_data_exercise.csv`** (~89MB, 645K rows) — mock UberEats order history with columns:
- `order_id`, `eater_id`, `merchant_id`, `courier_id`
- `order_timestamp`, `dropoff_timestamp`, `delivery_time_mins`
- `delivery_zip_code`, `restaurant_zip_code`
- `merchant_name`, `cuisine_type`, `merchant_activation_date`, `eater_account_creation_date`

**Public data sources** (to be sourced externally):
- NYC Restaurant Inspection Results
- US Census Data 2020 (ZCTA — zip code tabulation areas)
- NYC ZIP Code shapefiles (2020)

## Architecture

The exercise follows a standard ELT/analytics engineering pattern:

```
Raw Sources → Staging → Intermediate → Final Mart (zip_code_metrics)
```

**Conceptual final table:** one row per `(zip_code, dimension)` with aggregated metrics such as:
- Order volume and growth rate
- Merchant count and activation trends
- Market penetration (orders per capita from census data)
- Average delivery time
- Cuisine diversity / saturation indicators

## Key Evaluation Criteria

- **Strategic thinking**: clear prioritization framework with explicit trade-offs (growth vs. densification, saturated vs. untapped markets)
- **Data modeling**: normalized staging layers, clean grain definition, scalable ELT design
- **SQL proficiency**: window functions, CTEs, aggregations across zip × dimension combinations
- **Python**: automation, visualization (Streamlit preferred for bonus dashboard)
- **Communication**: ability to translate technical output into business insight

**Deliverables expected:**
1. Strategic framework + 3-5 core metrics (written explanation)
2. Conceptual data model + SQL queries producing a zip-code-level reporting table
3. (Bonus) Interactive Python dashboard (Streamlit or Jupyter Notebook)
4. Summary presentation (max 10 slides)

- **Framework**: Define a logical framework for prioritizing NYC postal codes for food delivery investment. What defines a "high potential" market versus a "saturated" or "low priority" market? Consider trade-offs like growth vs. densification.
- **Metrics**: Translate your framework into 3-5 core metrics. Explain the business rationale for each metric and how it informs decision-making.

## This is what we know:
- Average WoW growth of 14.6% across the period
- Order volume is geographically flat - top 10 zip codes contribute only 12.9% of total orders
- Supply directly drives demand, restaurant count is linearly proportional to order volume across all zip codes
- 75% of the orders were delivered within 45min of order placement

## Ideas 
- Use NYC Census data to map out the density of population in each zip code, compare it with current demand and supply
- Build a Dimensional zip table that should contains zipcode level data such as total population, area_sq_km, restaurant rating in that zip code


