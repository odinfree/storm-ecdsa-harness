// Toffoli-per-divstep cost model of a batched (jump-K) hddivstep update vs the elementary walk.
// Primitives: Gidney in-place adder A(m)=m; masked (quantum-controlled) add 2m; cswap m; signed unconditional add m.
function batch(K, m){
  const dec = 6*K*K;               // decision mini-walk on K-bit copies, forward+reverse
  const mat = 12*K*(K+1);          // build + uncompute 4 matrix entries (K+1 bits)
  const prod = 4*m*(K+4);          // 4 short-by-long products, signed-digit, out of place
  const adj = prod;                // adjugate uncompute of the old pair
  return {dec, mat, prod, adj, tot: dec+mat+prod+adj};
}
console.log("K  | per-step record (m=128) | per-step record (m=256) | per-step replay (m=256, +reduction 200/step) | floor 8m/K-terms");
for (const K of [4,8,16,32,62,64,128]){
  const r128 = batch(K,128).tot/K, r256 = batch(K,256).tot/K, rep = batch(K,256).tot/K + 200;
  console.log(`${String(K).padStart(3)} | ${r128.toFixed(0).padStart(6)} | ${r256.toFixed(0).padStart(6)} | ${rep.toFixed(0).padStart(6)} | 8m(1+4/K)=${(8*128*(1+4/K)).toFixed(0)} (m=128)`);
}
const K=16, L=544;
const b128 = batch(K,128), b256 = batch(K,256);
const B = L/K;
const recF = B*b128.tot, recR = recF, rep = B*(b256.tot + 200*K);
console.log(`\nK=${K}, L=${L}, B=${B} batches: record fwd ${recF.toLocaleString()} + record rev ${recR.toLocaleString()} + replay ${rep.toLocaleString()} = ${(recF+recR+rep).toLocaleString()} per operation; x2 operations + 44k shells = ${(2*(recF+recR+rep)+44000).toLocaleString()}`);
const Q = 256*4 + 512 + L + 4*(K+1) + 2*K + 256;
console.log(`Q = 4x256 payload/walk + 512 out-of-place pair + ${L} transcript + ${4*(K+1)} matrix + ${2*K} copies + 256 adder ancilla = ${Q}`);
console.log(`product = ${((2*(recF+recR+rep)+44000)*Q/1e9).toFixed(2)}e9  (incumbent 0.939e9, target 0.845e9)`);
