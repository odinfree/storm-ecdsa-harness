// Fraction of hddivsteps whose post-state delta' = 1/2 (branch 1 from delta=1/2 vs branch 2/3 from delta=-1/2 are
// indistinguishable from (delta',f',g') alone), i.e. steps whose swap bit must be stored in a Bezout-free transcript.
const p = (1n<<256n) - (1n<<32n) - 977n;
let s0 = 0x9E3779B97F4A7C15n, s1 = 0xD1B54A32D192ED03n;
function rnd64(){ let x=s0, y=s1; s0=y; x^=(x<<23n)&0xFFFFFFFFFFFFFFFFn; s1=x^y^(x>>17n)^(y>>26n); return (s1+y)&0xFFFFFFFFFFFFFFFFn; }
function rnd256(){ return (rnd64()<<192n)|(rnd64()<<128n)|(rnd64()<<64n)|rnd64(); }
let steps=0, amb=0, br=[0,0,0], maxF=0, maxG=0;
for (let i=0;i<5000;i++){
  let w=rnd256()%p; if (w===0n) w=1n;
  let d2=1n, f=p, g=w;
  while (g!==0n){
    if (g&1n){ if (d2>0n){ const t=g; g=(g-f)>>1n; f=t; d2=2n-d2; br[0]++; } else { g=(g+f)>>1n; d2=2n+d2; br[1]++; } }
    else { g>>=1n; d2=2n+d2; br[2]++; }
    steps++; if (d2===1n) amb++;
  }
}
console.log(`steps=${steps} branch shares: swap ${(br[0]/steps).toFixed(3)} add ${(br[1]/steps).toFixed(3)} halve ${(br[2]/steps).toFixed(3)}; P(delta'=1/2)=${(amb/steps).toFixed(3)} -> transcript bits/step = 1 + ${(amb/steps).toFixed(3)} = ${(1+amb/steps).toFixed(3)}`);
