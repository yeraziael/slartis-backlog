# Tests

- Manueller Job ueberholt einen wartenden Abo-Job.
- Zwei Moves in dieselbe Bibliothek laufen nicht gleichzeitig.
- Zehn Schreibjobs erzeugen einen abschliessenden Scan.
- Gueltiger Messenger-Link erzeugt genau einen Job; ungueltige oder gesperrte Quellen werden abgelehnt.
- Abo kann angelegt, pausiert, fortgesetzt und entfernt werden.
- Queue-Zahlen stimmen mit dem persistenten Zustand ueberein.
- Leerer Abo-Scan bleibt stumm; neuer Treffer erzeugt einen Ping.
