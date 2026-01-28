SELECT
symbol, 
current_price,
ROUND(day_high,2) As day_high,
ROUND(day_low,2) As day_low,
ROUND(day_open,2) As day_open,
ROUND(prev_close,2) As prev_close,
change_amount,
ROUND(change_percent,4) As change_percent,
market_timestamp,
fetched_at
from {{ ref('bronze_stg_stock_quotes') }}
where current_price IS NOT NULL