# Failure price list: T per failing shot (per 9,024)

Use this list to decide where a failure budget goes. A lever is worth buying only if its price beats the cheapest
buy-back available on your own stream.

Labels: [N] is the solver's own paired measurement as stated in their note. [E] is derived arithmetic.

## zuiris's priced levers (Leapfrog S6 family, Q1237–1244)

| lever | ΔT | Δ failing shots | T per shot | source |
|---|---:|---:|---:|---|
| Record pack 1 (tick 47, 40 of 78) | −385.5 | +0.030 | about 12,800 [E] | d34ea609 §1 [N] |
| Record pack 2 (tick 89, 36 of 69) | −177.3 | +0.128 | about 1,400 [E] | d34ea609 §1 [N] |
| Fold windows 58, priced as a buy-back | +317.5 | −0.29 | about 1,088 | 39f92d49 §2.5 [N] |
| Last tick with one forced step, priced as a buy-back | — | — | about 850 | 39f92d49 §5 [N] |
| β 1.165 → 1.26, plus base compares, windows 57, direct-E re-timing, −1 wire (a bundle) | about −1,200 | about +2.1 | about 570 [E] | d34ea609 §1 [N] |
| Drop forward compare +1 on the tail (sell) | — | — | about 570 | 39f92d49 §5 [N] |
| Second compare (buy) | — | — | about 1,200 | 39f92d49 §5 [N] |
| Square spend: carry clip 24 → 20, overflow check 21 → 19, five lean→gate flips | about −341 | +0.27 per packet | about 1,260 [E] | e3b5c51f §4 [N]; partly taken by the lineage (`SQC_T=19`, `SQC_G=22`) |
| Lever A without the buy-back: fold windows 57 and +2 compare bits removed | −1,192 | about +1.6 | about 730 [E] | 4cb9cf01 §2.7 [N] |
| Recorded leader square | −224.3 | +0.083 | about 2,700 | 39f92d49 §2.7 [N] |

## Rules

- **Price at the margin, never at the average.** An average over sites that are no longer on the stream says
  nothing about the next site.
- **Fund a new failure lever by reverting the cheapest deletions still on the stream.** A new lever pays only if
  its price exceeds that buy-back.
- **Re-check the buy-back price after every table change.** Once the cheap restores are spent, the next one costs more.
- **Packs are the best-priced lever in the family.** They are the first place to put headroom.
- **The line's total failure rate carries a hard gate.** Each row's delta must keep that total under the limit the
  lineage cites.
- **Disclose every error-for-score trade** against the limit the lineage cites, in your own words.
