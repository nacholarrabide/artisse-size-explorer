const fs = require('node:fs');
const vm = require('node:vm');
const assert = require('node:assert/strict');
const html = fs.readFileSync('contour.html', 'utf8');
const source = html.match(/<script id="geometry">([\s\S]*?)<\/script>/)[1];
const ctx = vm.createContext({});
vm.runInContext(source + '\nthis.api={radiusAt,wireLength,solveCup,validateState,catalogMatch,CATALOG,DEFAULTS,solveContact,contactGeometry,contactLengths,wallSlope,readScenario,PRESETS,sweepRange,experimentResult};', ctx);
const {radiusAt,wireLength,solveCup,validateState,catalogMatch,CATALOG} = ctx.api;
const DEFAULTS={...ctx.api.DEFAULTS,profile:'ellipse'};
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
 if(width>size){assert.equal(c.ok,true);assert.equal(c.reference,true);near(c.R,size/2);near(c.h,size*ratio);near(c.rimGap,(width-size)/2);continue;}
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

// Wall-following model: check length with a finer independent quadrature,
// exact contact, tangent continuity, monotonic free cap and wall clearance.
const {solveContact,contactGeometry,contactLengths,wallSlope,readScenario}=ctx.api;
let contactChecked=0;
for(const changes of [{},{contactMin:100},{contactMin:80},{turns:0},
 {turns:1.5},{ratio:.15},{ratio:.65},{neck:6},{neck:1,minPoleRadius:.02},
 {height:12,equator:8},{mode:'manual',rim:4},{mode:'manual',rim:1}]){
 const s={...ctx.api.DEFAULTS,...changes};
 const c=solveContact(s,s.size);
 assert.ok(c.ok,JSON.stringify(changes)+': '+c.reason);
 const g=contactGeometry(s,c.rim,c.detach,c.tailDepth);
 const fine=contactLengths(g,s.turns,4096);
 near(fine.length,c.L0,2e-6);
 near(c.contactWire+c.freeWire,c.L0,1e-8);
 assert.ok(c.relativeError<1e-9);
 assert.ok(c.poleRadius>=s.minPoleRadius);
 assert.ok(c.contactFraction>=s.contactMin/100-1e-8);
 assert.ok(c.penetration<=1e-6);
 near(g.wall(1).r,g.tail(0).r);near(g.wall(1).z,g.tail(0).z);
 near(g.tail(0).dr/g.tail(0).dz,wallSlope(c.detach,s));
 near(g.tail(1).r,0);near(g.tail(1).dz,0);assert.ok(g.tail(1).dr<0);
 for(let i=0;i<=10000;i++){
  const p=g.tail(i/10000);assert.ok(p.r>=-1e-9);assert.ok(p.dr<=1e-8);
  if(p.z>=0)assert.ok(p.r-radiusAt(p.z,s)<2e-6,'Free cap penetrates between validation samples');
 }
 for(const p of c.points.filter(p=>p.contact))near(p.r,radiusAt(p.z,s));
 contactChecked++;
}
const noLength=solveContact({...ctx.api.DEFAULTS,width:3,neck:2,height:14,equator:13,contactMin:100},5);
assert.equal(noLength.ok,false); // wall alone consumes more than available wire
const above=solveContact({...ctx.api.DEFAULTS,width:8,mode:'manual',rim:5.8},5);
assert.equal(above.ok,false); // nominal aperture enforced along whole wall segment
const old={...DEFAULTS};delete old.profile;delete old.contactMin;
const migrated=readScenario({model:'contour-cup-0.1',units:'mm',parameters:old});
assert.equal(migrated.profile,'ellipse');near(solveCup(migrated,9).h,solveCup(DEFAULTS,9).h);
assert.equal(readScenario({model:'contour-cup-0.2',units:'mm',parameters:ctx.api.DEFAULTS}).profile,'contact');
assert.throws(()=>readScenario({model:'future',units:'mm',parameters:DEFAULTS}));
assert.throws(()=>validateState({...ctx.api.DEFAULTS,contactMin:101}));
assert.throws(()=>validateState({...ctx.api.DEFAULTS,profile:'unknown'}));
console.log(`Contact: ${contactChecked} scenarios passed fine integration, wall clearance, tangency, contact, and import migration checks.`);

// Small cups remain visible and detached at the rim, including entirely
// intrasaccular cases and the comparison solver path.
for(const profile of ['ellipse','contact']){
 const s={...ctx.api.DEFAULTS,profile,width:10,neck:9,height:10,equator:5};
 const small=solveCup(s,5);
 assert.ok(small.ok&&small.reference&&small.undersized);
 assert.ok(small.pole>0);assert.equal(small.below,0);near(small.rimGap,2.5);
 assert.ok(small.points.every(p=>p.r<radiusAt(p.z,s)));
 near(small.h,5*s.ratio);assert.ok(small.relativeError<1e-10);
}
const fallback=solveCup({...ctx.api.DEFAULTS,width:3,neck:2,height:14,equator:13,contactMin:100},5);
assert.ok(fallback.ok&&fallback.reference&&!fallback.undersized);
assert.ok(fallback.referenceReason.includes('No adapted solution'));
for(const minPoleRadius of [.02,.1,.3,.5]){
 const s={...ctx.api.DEFAULTS,minPoleRadius};const c=solveContact(s,9);
 assert.ok(c.ok);assert.ok(c.poleRadius>=minPoleRadius);
 const g=contactGeometry(s,c.rim,c.detach,c.tailDepth);
 near(g.tail(1).dz,0);assert.ok(g.tail(1).dr<0);
 near(2*g.controlR*g.controlR/c.tailDepth,c.poleRadius);
}
const round=solveContact(ctx.api.DEFAULTS,9);
assert.ok(round.contactFraction>=.75&&round.contactFraction<=.85);
assert.throws(()=>validateState({...ctx.api.DEFAULTS,minPoleRadius:0}));
assert.ok(html.includes('lang="en"'));
console.log('Visibility, interior free cups, fallback silhouettes and minimum pole curvature checks passed.');

assert.equal(solveContact({...ctx.api.DEFAULTS,neck:1},9).ok,false);
assert.ok(solveCup({...ctx.api.DEFAULTS,neck:1},9).reference);

for(const patch of Object.values(ctx.api.PRESETS))validateState({...ctx.api.DEFAULTS,...patch});
assert.equal(validateState({...ctx.api.DEFAULTS,compare:-1}).compare,-1);
const bounds=ctx.api.sweepRange(ctx.api.DEFAULTS,'neck');near(bounds[1],ctx.api.DEFAULTS.width);
const referenceSample=ctx.api.experimentResult({...ctx.api.DEFAULTS,width:10,size:5},'contact');
assert.equal(referenceSample.status,'reference');assert.ok(Number.isFinite(referenceSample.depth));
console.log('Experiment presets, model comparison and sweep result classification passed.');
