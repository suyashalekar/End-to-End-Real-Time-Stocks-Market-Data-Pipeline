{{ config(materialized='table') }} -- Using table to fix DirectQuery

WITH source AS (
  SELECT
    symbol,
    current_price,
    market_timestamp
  FROM {{ ref('silver_clean_stock_quotes') }}
  WHERE current_price IS NOT NULL
),

all_time_volatility AS (
  SELECT
    symbol,
    -- We use standard deviation to calculate how much the price "jumps" (volatility)
    STDDEV_POP(current_price) AS volatility,             
    CASE
      WHEN AVG(current_price) = 0 THEN NULL
      ELSE STDDEV_POP(current_price) / NULLIF(AVG(current_price), 0)
    END AS relative_volatility
  FROM source
  GROUP BY symbol
)

SELECT
  symbol,
  volatility,
  relative_volatility
FROM all_time_volatility
ORDER BY symbol