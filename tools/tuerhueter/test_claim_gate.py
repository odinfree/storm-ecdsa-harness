#!/usr/bin/env python3
"""Both outcomes of claim-gate.py on a synthetic mailbox. Run: python3 test_claim_gate.py"""
import importlib.util, os
spec = importlib.util.spec_from_file_location('cg', os.path.join(os.path.dirname(os.path.abspath(__file__)), 'claim-gate.py'))
cg = importlib.util.module_from_spec(spec); spec.loader.exec_module(cg)
box = ['[lane-b] 01:10Z CLAIM 765 on TeamAccountA, submitting in 5 min',
       '  second line of the same post',
       'me: CLAIM 763 on TeamAccountB']
assert list(cg.open_claims(box, 'TeamAccountA', 'me')) == ['lane-b'], 'open claim by another lane must block'
assert cg.open_claims(box, 'TeamAccountB', 'me') == {}, 'own claim must not block'
assert cg.open_claims(box + ['[lane-b] 765 not submitted yet, still building'], 'TeamAccountA', 'me'), '"not submitted" keeps the claim open'
assert cg.open_claims(box + ['[lane-b] SUBMITTED 765 abcd1234'], 'TeamAccountA', 'me') == {}, 'SUBMITTED closes the claim'
assert cg.open_claims(['[lane-c] CLAIM: next free slot on either second account'], 'TeamAccountA', 'me'), '"either account" blocks both'
assert cg.open_claims(['otherlane: CLAIM 765 on TeamAccountB, submitting now'], 'TeamAccountB', 'me'), 'a "tag: ..." post by another lane must block'
assert cg.open_claims(['[ladderx] CLAIM 741 on TeamAccountA'], 'TeamAccountA', 'ladder'), 'a tag that merely starts with my name is another lane'
assert cg.open_claims(['[ladder-b] CLAIM 741 on TeamAccountA'], 'TeamAccountA', 'ladder') == {}, 'my own sub-lane does not block me'
two = ['[lane-b] CLAIM 765 on TeamAccountA', '[lane-b] 761 on TeamAccountB graded: accepted']
assert cg.open_claims(two, 'TeamAccountA', 'me', ['TeamAccountA', 'TeamAccountB']), 'a grade on another account leaves the claim open'
assert cg.open_claims(two, 'TeamAccountA', 'me') == {}, 'without CLAIM_ACCOUNTS any closing post by the tag closes (documented limit)'
print('claim-gate tests OK')
