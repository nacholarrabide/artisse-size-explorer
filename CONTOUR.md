# Contour geometry explorer v0.1

Open `contour.html` directly in a browser (offline), or serve this directory with
`python3 -m http.server 8765 --bind 127.0.0.1` and visit `/contour.html`.
No dependencies or build. This is a separate implementation; Artisse pages are unchanged.

## Model

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

## Verification

Run `node tests/contour.test.cjs`. Checks cover exact circular arc length at zero
twist, free-state recovery, length conservation across 198 feasible combinations,
unsupported overexpansion, wall collision, neck crossing, manual placement,
catalogue intervals and malformed scenario parameters.

## Data provenance and limitations

Catalogue: https://www.stryker.com/dk/en/neurovascular/products/contour-neurovascular-system.html
Accessed 2026-10-28. Sizes 5, 7, 9, 11 and 14 mm, with published sac/neck width
intervals. These are product-page data, not a replacement for applicable IFU.

No double layer, material law, friction, wire contact, release mechanics,
porosity or haemodynamics. Radial gaps and intersections in a symmetric section
are not circumferential apposition, neck coverage, or stability measurements.
Research/educational prototype; not validated for clinical use. Not affiliated
with Stryker or Medtronic. No proprietary model parameters or patient data included.
