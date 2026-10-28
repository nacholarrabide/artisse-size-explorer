# Contour geometry explorer v0.3

Open `contour.html` directly in a browser (offline), or serve this directory with
`python3 -m http.server 8765 --bind 127.0.0.1` and visit `/contour.html`.
No dependencies or build. This is a separate implementation; Artisse pages are unchanged.

## Original ellipse model

Synthetic axisymmetric single-envelope cup, with r=R sin(pi u/2),
z=zp+h(1-cos(pi u/2)), phi=2 pi n u, u in [0,1]. Reference wire length
is computed at nominal radius D0/2 and depth q D0; defaults q=.35 and n=.5
are arbitrary, not measured Contour parameters. Simpson integration (384 intervals)
and bisection solve for depth at the imposed local sac radius. Aperture greater
than nominal is outside this model. Geometry is checked at 401 profile points;
there is no wall clipping, mechanical contact solve, or claim of clinical fit.
The single curve is a meridional envelope, not a projected physical wire.

The sac uses cubic smoothstep below the equator and a quarter ellipse above it.
Four anatomy controls specify maximum width, height, equator height and neck width.
The rim can be fixed at the equator or positioned manually. Geometry and Stryker
catalogue interval matching are separate outputs. A second size can be overlaid.

In the default synthetic example the cup crosses the neck plane substantially.
This is an output of the uncalibrated assumptions, not a prediction of real Contour
behaviour. Vary q and n to inspect sensitivity; do not tune them to a desired
clinical conclusion. Calibration needs measured free and constrained profiles.

JSON export includes model version, units, parameters, source and derived results.
Import validates parameters and recomputes results (ignores imported results).
SVG export contains visible experimental-use text and scenario metadata.

## Wall-following model (default in v0.2)

The profile follows the actual sac wall from the rim to a searched detachment
height, then follows a quadratic Bezier cap to the proximal pole:
P0=(rA(zd),zd), P1=(rA(zd)-a*rA'(zd),zd-a), P2=(0,zd-a).
This enforces geometric tangent continuity (G1, not curvature continuity),
a horizontal tangent at the pole, and a monotonically narrowing free cap.
Degenerate caps with a zero terminal tangent are excluded.

The same reference wire budget L0 from the original model is retained. On the
adapted shape, total twist 2*pi*n is distributed uniformly per meridional arc
length S. Integrate sqrt(1+(r*2*pi*n/S)^2) ds over wall AND free cap; solve for a.
This is a different twist-distribution hypothesis from the ellipse's uniform
parameter-angle law. Do not interpret shape differences as contact mechanics alone.

Search 61 detachment heights from the requested minimum wall descent to the
neck, starting no higher than the equator. Each height has 16 depth brackets;
roots are bisected without assuming global length monotonicity. Only the first
sampled feasible configuration is chosen. Simpson integration uses 256 intervals
per segment, splitting the wall at the equator; admissible roots are refined
at 1024 intervals. Search results can change discretely with sliders.

Free-cap penetration is checked at 601 points, with a 1e-6 mm radial tolerance.
This is sampled feasibility, not a continuous nonpenetration proof. Below the
neck, no arterial boundary is invented; crossing remains visibly flagged.
No solution means none found in this particular family/search, not physical
impossibility. The minimum wall descent slider sets a lower bound on vertical
contact distance / rim height, not an adhesion or friction coefficient.

Amber marks the wall-following segment, circles mark departure, and the metrics
separate contact and free wire length. The numerical residual measures algebraic
closure only, not experimental accuracy. Old v0.1 JSON scenarios import into the
ellipse mode; v0.2 exports include the profile and minimum contact setting.

## Verification

Run `node tests/contour.test.cjs`. Checks cover exact circular arc length at zero
twist, free-state recovery, length conservation across 198 feasible combinations,
unsupported overexpansion, wall collision, neck crossing, manual placement,
catalogue intervals and malformed scenario parameters. An additional 12 contact
scenarios verify independent 4096-interval integration (absolute length error
below 2e-6 mm), tangent joins, contact tracking, 10,001-point free-cap clearance,
monotonic radius, minimum contact settings, and old-scenario migration. Also tests
search failure for insufficient wire and nominal limits along the wall path.

## Data provenance and limitations

Catalogue: https://www.stryker.com/dk/en/neurovascular/products/contour-neurovascular-system.html
Accessed 2026-10-28. Sizes 5, 7, 9, 11 and 14 mm, with published sac/neck width
intervals. These are product-page data, not a replacement for applicable IFU.

No double layer, material law, friction, wire contact, release mechanics,
porosity or haemodynamics. Radial gaps and intersections in a symmetric section
are not circumferential apposition, neck coverage, or stability measurements.
Research/educational prototype; not validated for clinical use. Not affiliated
with Stryker or Medtronic. No proprietary model parameters or patient data included.


## v0.3 visibility, pole roundness and English UI

All interface text, methods, SVG labels and runtime messages are in English.
An undersized device is no longer hidden: the display wrapper returns its
nominal-width, free-depth ellipse at the selected rim height, measuring each
radial gap to the wall. The shape is evaluated against the actual sac, so a
narrower lower wall can still intersect it. Fully intrasaccular cups stay visible.
If the adapted search fails, a labelled reference ellipse is displayed instead;
its warnings and exported metadata explicitly distinguish it from a contact
solution. The direct contact solver still reports infeasibility.

Contact caps now require pole curvature radius rho=2*controlR^2/depth >= an
editable bound, default 0.10 mm (range 0.02–0.50 mm). Horizontal tangent alone
was insufficient: nearly zero controlR produced a visually sharp tip nearby.
The default bound gives roughly 75–80% wall descent for the default anatomy;
this is a synthetic geometric setting, not a measured force or universal
contact percentage. This bound applies to the adapted cap, not reference
ellipses. v0.1 and v0.2 scenarios remain importable; v0.2 imports receive the
new default roundness setting. Exports use model version contour-cup-0.3.

Additional tests cover undersized silhouettes, gap measurements, fully internal
cups, visible search-failure fallbacks and several curvature bounds.


## Diameter interpretation and undersized colour

Undersized cups and their rim-gap annotations are entirely red, including in
comparison mode (dashed line still identifies the comparison). Other profiles
retain segment-level contact/conflict colours.

Stryker labels nominal sizes as device diameters. The source does not establish
the precise reference configuration; treating D0 as free rim span is explicitly
a model assumption pending confirmation. The UI and JSON now distinguish
nominal diameter, actual rim span 2R, and the complete meridional profile arc
through the pole (2S). That profile arc is not the helical wire length L0.

## Experiment bench

Six synthetic anatomy presets, session-memory scenario collection with JSON
roundtrip, and same-size other-model overlay are available. Parameter sweeps
sample 15 evenly spaced values while holding other inputs fixed. Invalid anatomy
samples are skipped; fallback silhouettes appear as red crosses and are never
connected into successful-model curves. Rings mark >0.5 mm changes between
adjacent valid points; this heuristic depends on sample spacing and is not a
clinical threshold. Changes invalidate old sweep results. Sweeps can be cancelled
between samples and exported with baseline settings and per-sample status.

Clinical calibration preparation is documented in CALIBRATION.md. No real case
data have been loaded, and the departure solver has not been altered by this step.

## Visual quick presets

Three clickable SVG anatomy thumbnails sit above the main explorer. They reset
model assumptions and turn comparison off, selecting C9, C7 and C5 respectively (Near-unit, Ovoid, Tall).
Their width/height dimensions are 8.4/8, 6.4/7.8 and 4.2/6.8 mm; the equator is
at half the sac height in all three. Neck widths remain 4.5, 4 and 2.2 mm.
These are synthetic exploration geometries, not selected fits: catalogue warnings,
neck crossing and reference fallback remain visible when applicable. Comparisons
can be enabled manually; both profiles are independently solved and the secondary
profile stays dashed, including contact and conflict segments. Both poles are labelled.

DEPLOY_CONTOUR_PROMPT.md contains a handoff prompt for AngioSeg integration, with destination verification.
No production deployment is performed by these changes.

The dark palette follows local AngioSeg web/src/index.css tokens, with system
sans typography matching its Tailwind sans default. No external fonts are loaded.
The user confirmed AngioSeg as the destination project.
