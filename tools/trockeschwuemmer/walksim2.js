const P=(1n<<256n)-(1n<<32n)-977n;
const abs=x=>x<0n?-x:x;
function v2(x){x=abs(x);let c=0;while((x&1n)===0n){x>>=1n;c++}return c}
function rnd(){let r=0n;for(let i=0;i<8;i++)r=(r<<32n)|BigInt(Math.floor(Math.random()*4294967296));return r%P}
// generic leapfrog: M forced odd-keeping steps, then optional choice step (deep candidate = 0 mod 4, strip up to cap extra zeros)
function lf(d,M,cap,choice){let T=(d&1n)?d:d+P,S=P,adds=0,halv=0,ticks=0,tape=0;
 while(!(abs(T)===1n&&abs(S)===1n)){
  for(let i=0;i<M;i++){const a=T+S,b=T-S;T=((a>>1n)&1n)?(a>>1n):(b>>1n);adds++;halv++;tape+=1;}
  if(choice){if(abs(T)===1n&&abs(S)===1n)break;const a=T+S,b=T-S;const deep=(((a%4n)+4n)%4n===0n)?a:b;const flat=(deep===a)?b:a;const e=v2(deep)-1;
   if(cap!==null&&e>cap){T=flat>>1n;halv++;}else{T=deep>>BigInt(e+1);halv+=e+1;}adds++;tape+=1+(cap===null?4:Math.ceil(Math.log2(cap+2)));}
  [T,S]=[S,T];ticks++;if(ticks>6000)return null;}
 return [adds,halv,ticks,tape];}
// Stein: subtract smaller from larger, strip zeros (cap on strip per add; leftover zeros strip next add)
function stein(d,ab,cap){let T=abs((d&1n)?d:d+P),S=P,adds=0,halv=0,tape=0,pend=0,pendOn=0;
 while(!(T===1n&&S===1n)){let big;
  if(ab===null)big=T>=S;else{const lt=T.toString(2).length,ls=S.toString(2).length;if(lt!==ls)big=lt>ls;else{const k=BigInt(Math.max(0,lt-ab));big=(T>>k)>=(S>>k);}}
  let D=big?T-S:S-T;if(D===0n)break;let v=v2(D);let s=(cap===null)?v:Math.min(v,cap);D>>=BigInt(v);
  // if strip capped, the leftover zeros cost extra 'strip-only' steps (counted as adds with zero addend)
  let extra=(cap===null)?0:Math.ceil((v-s)/cap);
  if(big)T=D;else S=D;adds+=1+extra;halv+=v;tape+=(1+extra)*(1+(cap===null?4:Math.ceil(Math.log2(cap+1))));
  if(adds>6000)return null;}
 return [adds,halv,adds,tape];}
const rules={
 "pingpong M=1":d=>lf(d,1,null,false),
 "leapfrog M=3 cap3":d=>lf(d,3,3,true),
 "leapfrog M=2 cap3 (HEAD)":d=>lf(d,2,3,true),
 "leapfrog M=1 cap3":d=>lf(d,1,3,true),
 "PM M=0 cap3":d=>lf(d,0,3,true),
 "PM M=0 cap7":d=>lf(d,0,7,true),
 "PM M=0 uncapped":d=>lf(d,0,null,true),
 "Stein exact cmp cap7":d=>stein(d,null,7),
 "Stein exact cmp cap3":d=>stein(d,null,3),
 "Stein exact cmp cap2":d=>stein(d,null,2),
 "Stein exact cmp cap1":d=>stein(d,null,1),
 "Stein 8bit cmp cap7":d=>stein(d,8,7),
 "Stein 3bit cmp cap7":d=>stein(d,3,7),
 "Stein bitlen cmp cap7":d=>stein(d,1,7),
};
const name=process.argv[2],n=parseInt(process.argv[3]||"1000");const f=rules[name];
const res=[];let fails=0;for(let i=0;i<n;i++){const r=f(rnd());if(r===null){fails++;continue}res.push(r)}
const col=j=>res.map(r=>r[j]);const mean=a=>a.reduce((x,y)=>x+y,0)/a.length;const q=(a,p)=>{const s=[...a].sort((x,y)=>x-y);return s[Math.min(s.length-1,Math.floor(p*s.length))]};
const A=col(0),H=col(1),Tk=col(2),Tp=col(3);
console.log(name.padEnd(26)+`| adds mean ${mean(A).toFixed(1).padStart(6)} p99 ${String(q(A,0.99)).padStart(4)} max ${String(Math.max(...A)).padStart(4)} | halv mean ${mean(H).toFixed(1).padStart(6)} max ${String(Math.max(...H)).padStart(4)} | ticks mean ${mean(Tk).toFixed(1).padStart(6)} p99 ${String(q(Tk,0.99)).padStart(4)} max ${String(Math.max(...Tk)).padStart(4)} | tape bits mean ${mean(Tp).toFixed(0).padStart(5)} max ${String(Math.max(...Tp)).padStart(5)} | fails ${fails}`);
