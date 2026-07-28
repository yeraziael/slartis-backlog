# Functional contract

## 1. Objective

KitchenOwl becomes the household system of record for stock, inferred consumption and shopping preparation. Shopping lists and recipes remain secondary to reliable inventory management.

## 2. Receipt intake

- Source: Paperless documents of type `Kassenbon`.
- Correspondent matching is case-insensitive; initial merchants: Rewe, Lidl, Netto, Kaufland and Aldi.
- Unknown correspondents and uncertain lines require operator review.
- Safe lines update stock immediately; uncertain lines can be corrected, mapped or skipped independently.
- Every line stores Paperless document ID, original text, merchant, quantity, unit, price, mapping version and confidence.
- Reprocessing is idempotent.

## 3. Product model

- Merchant items map to canonical household products.
- Brands merge by default unless a separate product is explicitly required.
- Consumption-relevant variants remain separate, including fat level, zero/regular, spicy/mild, gluten-free, lactose-free and sensitive variants.
- Physical quantity and normalized pack count are both stored.
- Reference pack size is learned from the most frequently purchased size; operator overrides persist.
- Preferred purchase size changes automatically only after another size dominates by receipt count in two consecutive calendar months; one receipt counts once per size.
- Product merges preserve the oldest reliable normalization history.
- Product splits require an admin proposal and apply only from the confirmed split time; shared history is allocated proportionally.
- Initial stock is proposed from historical receipts and must be confirmed.

## 4. Consumption and minimum stock

- Base consumption uses a rolling 12-week window.
- Confirmed manual list corrections adjust consumption directly; no retrospective redistribution across the 12-week window.
- Correction factors accumulate, may offset each other and may change direction.
- Their effect naturally grows out through newer data in the rolling window.
- Increased demand: automatic consumption-rate adjustment after three consecutive weeks at least 20 percent above prediction.
- Reduced demand: automatic consumption-rate adjustment after six consecutive weeks at least 20 percent below prediction.
- Minimum-stock changes are always proposed and require confirmation.
- Rate changes immediately recalculate all open weekly, monthly and MM lists, but only for open, non-protected quantities.

## 5. Shopping cycles

- Monthly forecast: five days before month end; list name `YYYY-MM`.
- Monthly purchase consists of qualified receipts from the last day of the previous month through the third day of the month and includes the first weekly shop.
- Weekly list is generated Thursday evening for Friday/Saturday; list name `YYYY-Woche_KW`.
- Friday and Saturday form the regular weekly purchase; Saturday closes it.
- Sunday is a follow-up day for open or incomplete positions.
- Purchases from Monday onward are stock-correcting top-ups and learning signals, not part of the closed weekly purchase.
- MM is a marked weekly list on the nearest Friday/Saturday no earlier than 14 days after the monthly purchase; suffix `-MM`.
- Partially bought quantities move to the next suitable list. Non-purchase does not reduce inferred need.
- Manually added or changed entries are protected from automatic removal or quantity changes.

## 6. Shelf-life classes

Each normalized product is operator-confirmed as:

- lightly perishable: weekly stocking only;
- limited shelf life: stocked at monthly purchase and MM cycle;
- shelf-stable: eligible for monthly stocking.

Limited shelf life is learned from purchase, stock and correction intervals.

## 7. Season and weather

- Seasonal products are detected automatically and shown with a soft season window.
- All available prior years contribute with exponentially declining weight.
- A household-wide consumption trend scales historical seasonal demand.
- Seasonal offer availability and seasonal/weather-dependent demand are separate models.
- Weather can propose a current-year season-window shift; confirmation is required and applies to all products in the inferred seasonal category.
- Weather-dependent quantity changes are proposals for the next suitable list only.
- If demand starts before the regular shop, stock is requested and a separate intermediate-shopping list may be proposed.
- Pre-season test stock is half a weekly quantity, has no effect on forecast or season learning, and loses test status when the season begins.
- Three weeks of non-purchase despite list presence softly end the season; omitted quantities are discarded.
- A single later purchase is a neutral tail purchase.
- Earlier or later purchases in two consecutive years are displayed; after three consistent years the season window may adjust automatically.

## 8. Household and location context

- Household: two adults and six children; ages advance automatically from birthdays.
- Move-in, move-out, long absence, temporary absence, guests and relocation are household events.
- Event-based changes to the household consumption factor are proposed, never applied blindly.
- The regular shopping area is learned from high-volume provisioning purchases of staples.
- Purchases more than 100 km from that area are excluded from forecasting as travel outliers.
- A second regular area is proposed as a move; during an approved transition both areas are valid.
- The new area replaces the old after confirmation. Dominance is based on provisioning quantity, not receipt count or value.

## 9. Occasions and personal demand

- Birthday windows learn between seven and fourteen days before the event.
- Shared birthdays use one marked occasion section in the next suitable shopping list.
- Positions can migrate until the occasion and at most through the first weekly purchase after it; that purchase remains an occasion expense.
- Occasion guest count is estimated. Only a manual guest-count change scales current occasion quantities.
- Scaling is category-specific and learned from prior occasions.
- Sparse data is conservatively rounded up; usable excess increases stock.
- After three comparable occasions with excessive product-specific remainder, a reduction is proposed.
- Personal demand is attributed to a participant but affects stock only; consumption remains inferred over time.
- A personal recurring pattern is proposed after five similar reports, first to the affected user.

## 10. Price and promotion logic

- Cost simulation uses the last confirmed regular price, matching pack and preferred merchant where possible.
- Suspected promotional prices require confirmation.
- Promotions update stock and price history but not regular-price forecasting.
- Repeating promotion patterns are announced with an optional stocking increase.
- Suggested additional quantity considers both expected savings and demand until the next likely promotion.
- Low savings do not hide the option.
- No fixed budget cap is configured; unusual proposals are only marked.
- Purchasing-power inference is internal, seasonal and separated from need. Special promotion purchases do not raise or lower it.

## 11. Model maturity

- Normal products become historically known after more than six months from reliable normalization.
- Seasonal products require 24 months.
- Stable purchase patterns require at least three matching cases.
- Historical products activate stable patterns automatically; new products notify admins.
- `stable since` is a calculated admin-only quality datum and may be backdated when later evidence improves the model.