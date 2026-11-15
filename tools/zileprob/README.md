# Zileprob (row rehearsal)

Technical id: `zeileprob.py`.

An exhaustive model that killed a lead before anyone built it. Runtime about ten seconds.

The lead ("Vorzeichezile", sign row) came from arXiv:2609.05625 (Häner, Tripier, Young et al., 2026), where a
binary-gcd iteration is rewritten so that every step is an uncontrolled add or subtract whose direction is
chosen by a sign, at 2 Toffoli per wire where a controlled, restoring step costs 3. The ring rows of the
frame under our 763 row (Akashneelesh's public row 8396ec91) are restoring rows at 3 Toffoli per wire, and they are 42.6 % of that
frame's static Toffoli count. A signed row would have been worth up to 2.65 million Toffoli per stream at
width 763.

The model takes the geometry of one multi-class digit slot (16 wires, 4 rows, classes 0 to 4, divisors below
32), enumerates all 169,136 cases, and compares four candidate forms with the restoring reference:

| form | Toffoli per plain wire | wrong after the ideal sign correction |
|---|---|---|
| A, unmasked, sign continues through inactive rows | 2 | 151,637 |
| B, unmasked, forced signs on inactive rows | 2 | 151,595 |
| C, carry masked, sum unmasked | 2 on the unmasked wires | 150,931 |
| D, mask and activity kept on the sum | 3 | 0 |

So the row's third Toffoli is not only the digit control. It also carries the class mask and the activity
gate, and those cannot be folded into the choice between add and subtract when one slot serves several
classes. The positive control confirms the model: with every row active and no foreign data below the
operand, form A is wrong in 0 of 7,936 cases. The lead stays closed unless a slot design gives each row a
single class.

## Run

```bash
python3 zileprob.py | diff - out_zileprob.txt && echo reproduced
```

No inputs. Output: the table above with per-class counts; `out_zileprob.txt` is the output we recorded on
15 Nov 2026.

## Limits

It is a 16-wire model of one slot, with the pairing and masking read from the frame's row emitter. It proves
one thing about the 256-bit circuit: the plain port is not exact. A different signed design may still exist. The other premises of the lead (the cofactor ring's erase, the page sandwich's digit reads)
were never tested, because this one failed first.
