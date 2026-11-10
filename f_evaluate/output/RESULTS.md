# Run results

## Analytic benchmark

- Pulse relative L1 cell-mass error at 20 s was 1.43% at 2 m, 0.34% at 1 m, 0.09% at 0.5 m.
- Finite-release crosswind profile relative L1 error was 0.76% at 2 m, 0.26% at 1 m, 0.14% at 0.5 m.

## Coastal carbon toy model

- The full run released 4,221.1 kg C and converted 158.0 kg C from VOC to aerosol.
- At the end, 25.0 kg C was in the land pool and 20.4 kg C in the ocean pool.
- Maximum absolute mass-balance residual across scenarios was 4.9e-11 kg C.

## Prairie Grass

Out-of-fold predictions cover 44 runs on 20 meteorological dates, with 4,747 arc measurements and 1,990 tower measurements from 37 runs. Values below are day-weighted RMS errors of log(1 + C / C₀), with C₀ = 1 mg/m³ by default.

| Model | Arc receptors | Sampled arc peaks | Tower receptors |
| --- | ---: | ---: | ---: |
| Briggs Gaussian, nominal | 2.063 | 1.003 | 1.258 |
| Briggs Gaussian, fitted | 1.589 | 1.273 | 1.274 |
| Wind-variability Gaussian | 1.649 | 1.324 | 1.470 |
| CA, flat wind | 1.647 | 1.318 | 1.470 |
| CA, shear | 1.659 | 1.332 | 1.517 |
| CA, deposition | 1.641 | 1.412 | 1.448 |
| CA, shear + deposition | 1.650 | 1.451 | 1.478 |
| CA, shear + higher deposition | 1.651 | 1.546 | 1.448 |

Paired changes for the shear-plus-deposition lattice versus its matched wind-variability Gaussian. Negative values favor the lattice. Intervals resample meteorological dates with fitted models fixed.

- Arc receptors **+0.001** [-0.033, +0.032]
- Sampled arc peaks **+0.127** [+0.079, +0.184]
- Tower receptors **+0.008** [-0.013, +0.033]

Deposition alone changed tower error by -0.022 and sampled arc-peak error by +0.095 relative to the flat-wind lattice.

- The matched flat-wind lattice and Gaussian differed by at most 0.031 RMS log1p across the two receptor arrays.
- Doubling resolution changed predictions by at most 0.059 RMS log1p in any audited run × array × model.
- Maximum relative flux ledger residual was 6e-15. The shear-plus-deposition run deposited 12.9% of emitted mass on average by the last downwind receptor plane.
- Width or bearing calibration reached a configured bound in 5 of 10 fits.

[Held-out scores](field_skill.pdf) · [Receptor profiles](field_profiles.pdf) · [Sampled arc peaks](field_arc_peaks.pdf)

See the CSVs for model contrasts, scores by radius, run-level flux accounting, and numerical refinement.
