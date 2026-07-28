# Release acceptance gates

## A. Data integrity

- [ ] Reprocessing a receipt cannot duplicate stock.
- [ ] Every stock mutation can be traced to receipt, measurement, correction or approved command.
- [ ] Skipping one receipt position never blocks valid sibling positions.
- [ ] Product merge and split operations preserve history according to the contract.
- [ ] Backup restore reproduces catalog, stock, list state, mappings, model metadata and audit history.

## B. Forecast correctness

- [ ] Golden tests cover increased demand after three weeks and reduced demand after six weeks.
- [ ] Minimum-stock changes never activate without required approval.
- [ ] Open protected or manually changed list positions are never overwritten.
- [ ] Monthly, weekly, MM and intermediate-list boundaries match the defined calendar rules.
- [ ] Seasonal offer, seasonal demand, weather demand, occasion demand and opportunity purchases remain distinct.
- [ ] Prediction calibration starts at ±20 percent and reaches no lower than ±5 percent only after three valid measurements on different days with predicted stock movement.
- [ ] Target-confidence products are remeasured only after a qualifying abnormal-replenishment pattern.

## C. Authorization

- [ ] Keycloak group removal immediately removes effective privileges.
- [ ] Every authenticated user can manage only their own demand by default.
- [ ] Family-demand, delegated-assignment, stock-maintenance and app-admin rights are separately testable.
- [ ] Provisional assignments by Cati or Nana require admin approval unless self-assigned.
- [ ] Stock-maintenance users cannot access global quality, audit, purchasing-power or occasion-admin data.

## D. Signal and Matrix

- [ ] Initial critical alerts are immediate.
- [ ] Escalations occur only on the hour from 07:00 through 21:00 Europe/Berlin.
- [ ] Reading does not acknowledge an alert; an explicit admin action does.
- [ ] Per-admin mute lasts through end of day without muting other admins.
- [ ] Reminder count remains cumulative and deadline remaining is displayed.
- [ ] Stock requests obey weekday and weekend send windows.
- [ ] One product is asked per message, reply unit is explicit and zero synonyms are parsed.
- [ ] Latest valid reply before 23:59 wins; later replies cannot mutate stock.
- [ ] Runs stop at ten products and require ad-hoc admin continuation.

## E. UI

- [ ] Full admin dashboard is integrated into KitchenOwl web.
- [ ] Homelab dashboard exposes only compact status and a deep link.
- [ ] Stock-maintenance product list supports confidence, age, occasion, usefulness, category and shelf-life filters.
- [ ] Voluntary measurements are immediate web actions and do not send Signal group messages.
- [ ] Successful voluntary measurements remove personal watchlist entries.
- [ ] Product split and initial-stock proposals show before/after impacts and require confirmation.

## F. Rollout

- [ ] Historical import runs first in dry-run mode.
- [ ] Shadow-mode predictions are compared with real measurements before automatic rate changes are enabled.
- [ ] All unresolved mappings are visible and exportable.
- [ ] At least one monthly cycle, one MM cycle and four weekly cycles complete without integrity errors.
- [ ] Admins can disable ingestion, forecasting and notifications independently without losing data.
- [ ] Rollback procedure is tested and documented.

## Definition of done

A workstream is done only when implementation, automated tests, operational documentation, observability and migration/rollback evidence are committed. The project is releasable only when all applicable gates above pass and #112 links to the exact plan revision used for rollout.