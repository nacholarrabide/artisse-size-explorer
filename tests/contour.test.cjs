const fs = require('node:fs');
const vm = require('node:vm');
const assert = require('node:assert/strict');
const html = fs.readFileSync('contour.html', 'utf8');
const source = html.match(/<script id="geometry">([\s\S]*?)<\/script>/)[1];
const ctx = vm.createContext({});
vm.runInContext(source + '\nthis.api={radiusAt,wireLength,solveCup,validateState,catalogMatch,CATALOG,DEFAULTS};', ctx);
const {radiusAt,wireLength,solveCup,validateState,catalogMatch,CATALOG,DEFAULTS} = ctx.api;
const near=(a,b,tol=1e-8)=>assert.ok(Math.abs(a-b)<tol, `${a} != ${b}`);
near(radiusAt(0,DEFAULTS),2.25);near(radiusAt(3,DEFAULTS),3);near(radiusAt(6,DEFAULTS),0);
// Independent exact circular-meridian limit (no azimuthal twist).
near(wireLength(3,3,0),3*Math.PI/2);
// Recover the prescribed free depth when unconstrained at nominal aperture.
for(const size of [5,7,9,11]){
 const s={...DEFAULTS,width:size,neck:2,height:14,equator:7};
 near(solveCup(s,size).h,size*s.ratio);
}
// Compression must preserve reference length, deepen this family, and stay finite.
let checked=0;
for(const size of [5,7,9,11,14])for(const ratio of [.15,.35,.65])for(const turns of [0,.5,1.5])for(const width of [2,3,5,7,10,12]){
 const s={...DEFAULTS,size,ratio,turns,width,neck:Math.min(width,4.5)};
 const c=solveCup(s,size);
 if(width>size){assert.equal(c.ok,false);continue;}
 assert.ok(c.ok);assert.ok(c.relativeError<1e-10);assert.ok(c.h>=size*ratio-1e-8);
 assert.ok(c.points.every(p=>Number.isFinite(p.z)&&Number.isFinite(p.r)));checked++;
}
const large=solveCup({...DEFAULTS,width:2,neck:1},14);
assert.ok(large.below>0);assert.ok(large.points.some(p=>p.outside));
// Find wall collision within the sac, independently of neck-plane crossing.
const collision=solveCup({...DEFAULTS,width:6,neck:1,height:14,equator:10},7);
assert.ok(collision.penetration>0);assert.equal(collision.below,0);
assert.equal(catalogMatch(CATALOG[2],DEFAULTS),true);
assert.equal(catalogMatch(CATALOG[1],DEFAULTS),false);
assert.throws(()=>validateState({...DEFAULTS,neck:9}));
assert.throws(()=>validateState({...DEFAULTS,turns:NaN}));
assert.throws(()=>validateState({...DEFAULTS,mode:'bad'}));
assert.throws(()=>validateState({...DEFAULTS,equator:6}));
assert.equal(validateState({...DEFAULTS}).size,9);
// Manual rim sets aperture from local anatomy, not maximum width.
const manual=solveCup({...DEFAULTS,mode:'manual',rim:1},9);
near(manual.R,radiusAt(1,DEFAULTS));near(manual.pole+manual.h,1);
console.log(`Contour: ${checked} feasible parameter combinations; geometry, collisions, catalogue and import checks passed.`);
