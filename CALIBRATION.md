# Contour: paired-surface calibration protocol

Status: preparation only. No clinical surfaces have been loaded or used to fit
parameters. The current explorer remains synthetic and unvalidated.

## Required inputs, stored outside this public repository

For each de-identified case, supply the sac surface, implanted-device surface,
implanted nominal size and model, mesh format and physical units. Record whether
both surfaces already share coordinates; otherwise preserve the registration
transform and its provenance. Identify whether the sac is pre- or post-treatment,
image timing, attached/detached device state, and segmentation uncertainties.
Do not infer millimetres from an STL file or assume that matching bounding boxes
establish alignment. Never use the implanted device to deform the sac in order
to improve a fit. A rigid registration may be necessary; document residual error.
Keep raw data and derived case measurements outside this checkout and preview
server. Public commits must contain only synthetic examples and generic code.

## Stage 1: geometry and quality checks

Inspect units, connected components, degenerate triangles, orientation, open
boundaries, vessel branches and segmentation artifacts. Establish a reproducible
neck plane, normal pointing into the sac and anatomical origin. Preserve original
surfaces. Do not silently cap holes or discard components. Record inclusion and
exclusion decisions per measurement, not only per case.

## Stage 2: observed geometry

Extract sections at fixed physical spacing relative to the neck. Keep original
section contours and report equivalent diameter, minimum/maximum widths, centroid
shift and asymmetry. Do not reduce an asymmetric sac to a single diameter without
retaining that loss of information. Inspect multiple meridional orientations.

For the device measure rim geometry, rim height/orientation, pole, depth, profile
and spatial gap to the sac. Specify whether the segmentation represents an outer
envelope, individual wires, both layers or artifacts. Do not infer wire length,
porosity, force or friction from an envelope alone. Define a contact tolerance
from segmentation/registration uncertainty, not a universal zero-distance test.

## Stage 3: fit a reduced model

First evaluate the model at the observed pose (conditional shape experiment),
then evaluate any pose prediction separately. Using observed rim height is not a
validation of predicted placement. Keep a baseline with fixed parameters.

Fit a small set of global or size-dependent parameters; begin with q, n and the
pole-radius bound. Examine sensitivity and parameter tradeoffs before adding
coefficients. Many parameter sets may explain the same envelope: shape agreement
does not identify actual braid construction or material mechanics.

Use physical-distance profile errors, depth/pole errors and gap-profile errors
as separate endpoints. Avoid allowing many sections from one case to dominate
an objective. Record every fit's model version, input provenance, parameter bounds,
training case IDs, exclusions and residuals. Store these records privately.

## Stage 4: validation

Split by case/patient before tuning; if repeated acquisitions share a patient,
keep them in one split. For small cohorts consider grouped cross-validation,
with tuning restricted to the training groups. Evaluate held-out whole cases,
including sizes and shapes with poor fit; do not silently substitute reference
ellipses as successful predictions. Report failure frequency separately.

Assess segmentation/registration sensitivity and outliers before assigning
accuracy claims. No numerical acceptance threshold has yet been established.
A good axisymmetric fit does not establish 3D circumferential apposition or
clinical efficacy. If persistent angular asymmetry dominates error, retain the
2D explorer as an inspection tool and develop an explicit 3D model separately.

## Development sequence and current checkpoint

1. Reproducible synthetic presets and saved sessions: implemented.
2. Same-size model overlays and parameter sweeps: implemented.
3. Candidate departure/continuity selection: pending; baseline unchanged so the
   sweeps can first reveal where discrete selection causes jumps. Rings mark
   adjacent changes >0.5 mm only as an exploratory flag, not a solver failure.
4. More flexible free cap: pending comparison against measured profiles; current
   minimum pole radius already separates pole roundness from minimum contact.
5. Surface ingestion and calibration: waiting for file location/format, units,
   registration information and implanted-size mapping. No parameters fitted yet.
