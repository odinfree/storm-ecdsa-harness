# Skill: Funding-Carry Hunt (cross-venue, delta-neutral)

Use when two or more perp venues are controlled via API and you want market-neutral
yield without directional risk or a Binance/CEX dependency.

## Goal

Capture the funding-rate spread between venues while holding zero net delta. The trade is
LONG on one venue + SHORT the same asset on another, equal notional — price moves cancel,
funding accrues.

## Core rule (get the legs right)

- OPPOSITE funding signs across venues → short the +funding venue AND long the −funding
  venue = you RECEIVE funding on BOTH legs ("both-legs-pay"). Best case.
- SAME sign → short the higher-|funding| venue, long the lower = capture the SPREAD only.
- NEVER "short both" or "long both" — that is not delta-neutral (a real bug that mislabels
  same-sign pairs; always one long + one short).

## Method

1. Pull funding from every controlled venue; annualize (Extended hourly×24×365, Paradex/
   Binance 8h×3×365).
2. Rank shared assets by neutral carry; filter to holdable liquidity (skip thin books).
3. PLAUSIBILITY gate: a huge carry on a liquid pair is usually a stale/half-quote or a
   unit error, not free money — verify before sizing.
4. Fees: only net-positive if both legs are maker/zero-fee (perp+perp, no spot swap). A
   spot hedge (AMM swap) adds friction that eats small carries → net-negative sub-scale.
5. Size: both legs equal notional; rebalance if either leg's size drifts.

## Public boundary

No keys, account ids, or private balances in shared notes — venues + funding numbers only.

## Reference impl

welttowelt/supervega-trader: scripts/carry2.py (Paradex×Extended), scripts/carry-hunt.js
(Binance×Extended). Verified live 2026-07-04: MON +24.6%, AAVE +16.5% both-legs-pay.
