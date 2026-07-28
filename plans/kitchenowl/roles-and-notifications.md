# Roles and notifications

## Keycloak-derived permissions

Every authenticated user may manage their own personal demand.

Additional groups:

- `kitchenowl-family-demand`: change family demand.
- `kitchenowl-demand-assignment`: assign demand to another household member.
- `kitchenowl-stock-maintenance`: view restricted product-confidence list and submit stock measurements.
- `kitchenowl-app-admin`: global approvals, household events, forecast decisions, shopping-area changes, notification decisions and administrative dashboard.

Michael manages group assignment. Georgina may receive app-admin membership until manually revoked. Group removal immediately removes the corresponding permissions and notification routing without deleting decisions or history.

## Household demand assignment

- Georgina and Michael may change family demand and assign individual demand.
- Cati/Catalejah and Nana/Teresah may freely manage and self-assign their own demand.
- Their assignments to Mama, Papa or Family remain provisional until an app-admin approves them.
- Ayden, Lala/Alaric, Raggy/Ragnar and Bailey initially report through Michael, Georgina, Cati or Nana.
- When granted direct KitchenOwl access through Keycloak, they may manage and confirm their own demand.

## Signal and Matrix

- Phone number is stored during registration and a Signal account is linked.
- Delivery is routed through the household Matrix server and Signal bridge.
- Time-critical messages go to every current member of `kitchenowl-app-admin`.
- Reading is not acknowledgement. At least one admin must perform an action.

Valid admin actions:

- confirm;
- reject;
- change quantity;
- take responsibility;
- mute for the acting admin until end of day.

Confirmation of an intermediate purchase creates its dedicated list. Rejection closes it without a list. A valid terminal action closes the alert for all admins.

## Escalation

- Initial time-critical notification is sent immediately.
- Until an admin acts, reminders are sent on the hour between 07:00 and 21:00 Europe/Berlin.
- Notifications after 21:00 are delivered immediately but are first escalated at 07:00 the next day.
- Reminder counter continues for the entire lifetime of the open alert.
- Every reminder includes remaining time to deadline and the reminder count.
- Per-admin muting does not mute other admins.

Time-critical classes include stock shortages, weather-driven intermediate purchases, approvals before weekly/monthly/MM shopping, approvals before occasions and blocked or expiring list decisions.

## Stock-maintenance requests

- Weekdays may be sent only between 16:30 and 18:00.
- Weekends may be sent only between 12:00 and 18:00.
- One Signal message asks about one product and explicitly specifies the unit.
- Replies are accepted until 23:59 on the request day.
- A numeric reply is stored as total stock in the specified unit.
- `keine`, `keine mehr`, `ist leer`, `ist alle` and numeric zero mean stock zero.
- Further replies to the same request before expiry are corrections; the newest valid answer wins.
- Other stock maintainers are informed `Bestand erfasst`, then the next product is requested.
- At most ten products are queried per run. Admins decide ad hoc whether and how to continue and may reprioritize the remaining products.
- Requests do not escalate.
- An unanswered request expires at 23:59 and is not repeated automatically.
- Admins receive a link to manual stock entry with product and unit preselected.

## Manual web stock entry

- Entry is always a total stock, never a relative delta.
- A deviation over 20 percent from the previous value requires a confirmation preview.
- Signal replies do not use this 20-percent confirmation gate.
- A statistically unusual consumption drop inferred from a Signal stock correction triggers an informational admin notice only when product-specific consumption dispersion marks it as abnormal.
- Admins may use that notice to request measurements for related products when doing so provides real diagnostic value.

## Stock-maintenance dashboard access

Members may see only:

- product name;
- confidence value;
- stability status;
- last measurement;
- whether a new measurement is useful.

They may filter and sort by confidence, measurement age, occasion relevance, measurement usefulness, product category and shelf-life class. They may submit voluntary measurements directly in the web UI without generating a Signal group message and maintain a private watchlist. A successful measurement removes the product from that user's watchlist.