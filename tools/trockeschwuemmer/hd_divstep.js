// Half-delta divstep termination statistics on secp256k1 p, plus K-step transition-matrix NAF weights.
const p = (1n<<256n) - (1n<<32n) - 977n;
// xorshift128+ PRNG -> 256-bit random
let s0 = 0x9E3779B97F4A7C15n, s1 = 0xD1B54A32D192ED03n;
function rnd64(){ let x=s0, y=s1; s0=y; x^=(x<<23n)&0xFFFFFFFFFFFFFFFFn; s1=x^y^(x>>17n)^(y>>26n); return (s1+y)&0xFFFFFFFFFFFFFFFFn; }
function rnd256(){ return (rnd64()<<192n)|(rnd64()<<128n)|(rnd64()<<64n)|rnd64(); }

function hdSteps(w){ // delta2 = 2*delta, starts at 1 (delta=1/2)
  let d2=1n, f=p, g=w, n=0;
  while (g !== 0n){
    if (g & 1n){
      if (d2 > 0n){ const t=g; g=(g-f)>>1n; f=t; d2=2n-d2; }
      else { g=(g+f)>>1n; d2=2n+d2; }
    } else { g>>=1n; d2=2n+d2; }
    n++;
  }
  return n;
}
function nafWeight(x){ if (x<0n) x=-x; let w=0; while (x){ if (x&1n){ w++; if ((x&3n)===3n) x+=1n; else x-=1n; } x>>=1n; } return w; }
function kstep(d2,f,g,K){
  let u=1n,v=0n,q=0n,r=1n;
  for (let i=0;i<K;i++){
    if (g & 1n){
      if (d2 > 0n){ const t=g; g=(g-f)>>1n; f=t; d2=2n-d2; [u,v,q,r]=[2n*q,2n*r,q-u,r-v]; }
      else { g=(g+f)>>1n; d2=2n+d2; [u,v,q,r]=[2n*u,2n*v,q+u,r+v]; }
    } else { g>>=1n; d2=2n+d2; u*=2n; v*=2n; }
  }
  return [d2,f,g,u,v,q,r];
}
const N = parseInt(process.argv[2]||"20000");
const t0=Date.now();
const steps=[];
for (let i=0;i<N;i++){ let w=rnd256()%p; if (w===0n) w=1n; steps.push(hdSteps(w)); }
steps.sort((a,b)=>a-b);
const mean=steps.reduce((a,b)=>a+b,0)/N;
const q=x=>steps[Math.min(N-1,Math.floor(x*N))];
console.log(`N=${N} mean=${mean.toFixed(1)} min=${steps[0]} max=${steps[N-1]} q50=${q(0.5)} q90=${q(0.9)} q99=${q(0.99)} q999=${q(0.999)} q9999=${q(0.9999)} (${((Date.now()-t0)/1000).toFixed(0)}s)`);
for (const cut of [480,490,500,510,515,520,525,530,533,540,550]) console.log(`  P(steps > ${cut}) = ${(steps.filter(s=>s>cut).length/N).toExponential(2)}`);
for (const K of [16,32,62]){
  let tot=0,cnt=0,maxw=0, maxEntry=0n;
  for (let i=0;i<1000;i++){
    let w=rnd256()%p; if (w===0n) w=1n;
    let d2=1n,f=p,g=w;
    for (let b=0;b<Math.floor(590/K);b++){
      let u,v,q_,r; [d2,f,g,u,v,q_,r]=kstep(d2,f,g,K);
      const wt=[u,v,q_,r].reduce((a,x)=>a+nafWeight(x),0);
      tot+=wt; cnt++; if (wt>maxw) maxw=wt;
      for (const x of [u,v,q_,r]){ const ax = x<0n?-x:x; if (ax>maxEntry) maxEntry=ax; }
      if (g===0n) break;
    }
  }
  console.log(`K=${K}: mean total NAF weight of (u,v,q,r) = ${(tot/cnt).toFixed(1)} (per step ${(tot/cnt/K).toFixed(2)}), max ${maxw}; max |entry| = 2^${maxEntry.toString(2).length-1}.x`);
}
