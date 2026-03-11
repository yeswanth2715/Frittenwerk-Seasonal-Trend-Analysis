# Inventory Ordering Observation

## Workflow extension
After identifying seasonal demand patterns, the workflow was extended into inventory ordering to test how operational stock decisions could follow the sales signal.
- Monday delivery cycle: covers Tuesday, Wednesday, and Thursday.
- Thursday delivery cycle: covers Friday, Saturday, and Monday, with Sunday treated as spillover because the data includes Sunday trading.
- Stock order volume was estimated from cycle unit demand using a 20% to 25% rule based on the sales band.

## What the inventory layer checks
- Whether festival periods push teams to add extra stock above the base rule.
- Whether 3k-5k sales days still create wastage when order value becomes inconsistent.
- Whether product-mix shifts, especially poutine-heavy demand, distort stock ordering and expiry risk.

## Observations
- Total estimated excess stock across the modelled cycles: 5,971.9 units.
- Overall estimated wastage rate: 4.8%.
- Festival-linked wastage cases: 34.
- Low-sales but inconsistent-order-value cases: 17.
- Product-mix volatility cases: 33.
- Highest-risk cycle: 2025-12-11 (Thursday Delivery) with 213.9 excess units.
- Main driver in that cycle: Festival stock uplift.
- Observation note: Extra Christmas-market stock increased expiry risk.

## Interpretation
The seasonal signal is useful for labour planning, but it should not automatically become an aggressive inventory uplift. Festival periods can justify extra stock, yet repeated blanket uplifts raise expiry risk when actual basket mix or order value does not land where expected.
The same issue appears in some 3k-5k sales cycles: sales stay moderate, but volatile order value and product preference shifts can still lead to inconsistent stock ordering and avoidable wastage.
