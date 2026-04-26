# Casablanca Stock Exchange (Bourse de Casablanca)

The Casablanca Stock Exchange (CSE) is Morocco's sole stock exchange, founded in 1929.
It is regulated by the **Autorité Marocaine du Marché des Capitaux (AMMC)**.

Website: <https://www.casablanca-bourse.com>

---

## Market Indices

### MASI — Moroccan All Shares Index

- **Scope:** Tracks *all* listed companies on the CSE (~78 securities).
- **Methodology:** Free-float, capitalization-weighted. Market cap is adjusted to
  exclude shares held by major stakeholders, so only publicly tradeable shares count.
- **Base value:** 1,000 points (December 31, 1991).
- **First published:** January 1, 2002.
- **Purpose:** Primary benchmark for the Moroccan equity market. Used to evaluate
  mutual fund performance and portfolio returns.

### MADEX — Moroccan Most Active Shares Index (retired)

- **Scope:** Tracked the most actively traded (liquid) shares on the CSE.
- **Selection:** Shares chosen based on liquidity over the previous six months,
  considering market cap and trading volume.
- **Methodology:** Free-float weighted (since 2004). Price-only index (excludes dividends).
- **Rebalancing:** Twice yearly — June and December.
- **First published:** January 1, 2002.
- **Retired:** Calculation ceased January 1, 2022, replaced by the MSI 20.

### MSI 20 — Morocco Stock Index 20 (current reference index)

- **Launched:** December 2020; became the official reference index on January 1, 2022.
- **Scope:** 20 companies selected from the 40 largest by free-float capitalisation,
  filtered by trading volume and quotation frequency.
- **Purpose:** Captures the performance of the most liquid companies. Designed to align
  with international index best practices while reflecting Moroccan market specifics.

---

## Trading Hours

The CSE operates **Monday to Friday** in the **GMT+1 (Africa/Casablanca)** timezone.

### Regular Session (Segment 01 — Continuous Trading)

| Session               | Start    | End             |
|-----------------------|----------|-----------------|
| Pre-Trading           | 08:10    | 09:00           |
| Opening Auction Call  | 09:00    | 09:30 + T0*     |
| Regular Trading       | ~09:30   | 15:20           |
| Closing Auction Call  | 15:20    | 15:30 + T1*     |
| Closing Price Cross   | ~15:31   | ~15:40          |
| Post Close            | ~15:40   | ~15:55          |

### Ramadan Session (shortened hours)

| Session               | Start    | End             |
|-----------------------|----------|-----------------|
| Pre-Trading           | 08:10    | 09:15           |
| Opening Auction Call  | 09:15    | 10:00 + T0*     |
| Regular Trading       | ~10:00   | 13:20           |
| Closing Auction Call  | 13:20    | 13:30 + T1*     |
| Closing Price Cross   | ~13:31   | ~13:40          |
| Post Close            | ~13:40   | ~13:55          |

\* T0, T1, T2, T3 are random durations up to 180 seconds, determined automatically
by the system per instrument to prevent order-book manipulation at session boundaries.

### Market Segments

| Group | Description                                                    |
|-------|----------------------------------------------------------------|
| 01    | Shares traded in continuous trading session                    |
| 03    | Shares traded in single auction per session                    |
| 04    | Secondary lines (related to Group 01), single auction          |
| 05    | Secondary lines (related to Group 03), single auction          |
| 06    | Bonds traded as % of nominal value, single auction             |
| 07    | Bonds traded as monetary price, single auction                 |

---

## Key Holidays (2026, approximate)

- Labour Day — May 1
- Eid al-Adha — ~May 27-28
- Islamic New Year — ~June 16
- Throne Day — July 30
- Revolution Day — August 20
- Youth Day — August 21
- Green March Day — November 6
- Independence Day — November 18

Islamic holidays are based on the lunar calendar and dates shift each year.

---

## Useful Links

- [Live market data](https://www.casablanca-bourse.com/en/live-market)
- [Index history](https://www.casablanca-bourse.com/en/index-history)
- [Trading hours (official)](https://www.casablanca-bourse.com/en/trading-hours)
