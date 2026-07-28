# Forecasting and inventory model

## Core state

Each normalized product stores current stock, unit, normalized packs, base consumption rate, minimum stock, shelf-life class, confidence, season model, active correction factors and provenance.

## Prediction and measurement

- Model quality compares predicted stock with measured stock.
- Relative deviation is `(measured - predicted) / predicted`.
- Predicted zero uses an explicit zero-baseline branch and must never divide by zero.
- Initial tolerance is ±20 percent.
- Tolerance may fall by five percentage points per completed month down to ±5 percent.
- A reduction requires three qualifying measurements in the same calendar month, each on a different day and inside the current tolerance.
- A measurement qualifies only when a stock change was predicted since the previous qualifying measurement.
- At the ±5-percent target, scheduled calibration stops. Measurement resumes only when purchasing behavior suggests renewed deviation.
- If deviation later rises, admins choose whether to raise tolerance, retain ±5 percent with more measurements or set an intermediate product-specific tolerance.
- Any raised tolerance again decays by five percentage points per qualified month.

## Measurement frequency

When a product is outside tolerance, stock may be requested as frequently as every three days. Standard query priority follows lowest prediction confidence. Occasion-related queries outrank confidence-only queries.

At target confidence, a new query trigger requires a pattern of three abnormal replenishments within three months.

An abnormal replenishment must jointly indicate exhausted stock:

- timing is unexpectedly early;
- quantity is too small for stock-up;
- quantity is too large for a casual top-up;
- time and quantity together imply the predicted stock was exhausted.

A low or confirmed promotional price instead classifies the purchase as an opportunity purchase and not as consumption-model deviation. Product-specific quantity distributions learn the boundaries between small top-up, opportunity purchase and stock-up. A stable pattern requires at least three matching cases.

## Corrections and learning

- Manual stock corrections are interpreted through net normalized-pack deviation over an eight-week window.
- Four corrections in that window may propose a stocking adjustment.
- Proposed magnitude uses the median corrected deviation and rounds upward to whole packs.
- Correction down means consumption was higher than estimated; correction up means consumption was lower.
- No artificial maximum stock quantity exists.
- Operator overrides always win.
- Single peaks are marked as outliers first and may carry an exclusion reason. Only a confirmed pattern in a later weekly cycle may adjust normal consumption.

## Monthly stock-up

A monthly stock-up pattern combines purchase timing near the last working day, unusual quantity, higher receipt impact and recurrence. It becomes automatic after three comparable patterns. Bootstrap scans 24 months; ongoing detection uses a rolling 12-month horizon.

- A replenishment during the month means the monthly stock was exhausted by that point.
- Regular replenishment in at least four of the last eight weeks increases proposed monthly stock by median replenishment quantity.
- No purchase for two full months halves proposed stock repeatedly down to one normalized pack.
- Two further buyless months at one pack propose removing regular-stock status while retaining catalog and history.
- If monthly stock lasts beyond the next monthly purchase, quantity was excessive only after season, weather and occasion context are excluded.
- Three comparable excessive-stock cycles within 12 months are required before proposing reduction.

## Seasonal demand and household trend

All available same-month historical values contribute with exponentially declining weight. A household-wide consumption trend scales them. Household events may explain structural change, but any resulting factor change is proposed to admins.

Weather may affect demand separately from product availability. Weather-driven demand changes never apply automatically; they produce a proposal for the next suitable list. If expected demand begins before the next weekly shop, the system requests current stock and may propose a separate intermediate-shopping list.

## Confidence and quality

Per-product confidence considers normalization quality, prediction error, measurement recency, data volume, unresolved receipt lines and correction frequency.

`Stable since` is an admin-only calculated quality value. It may move backward when improved historical mapping or forecasting demonstrates earlier stability and has no behavioral effect.

A global app-quality metric is available in the full admin dashboard and is derived from stable-product share, average prediction error, normalization quality, unresolved positions and correction burden.