# Gaussian plume and local lattice transport

This project runs three experiments. It compares a three-dimensional Moore-neighborhood cellular automaton with an analytic dispersion model, toggles local processes in a synthetic mountain-to-ocean carbon model, and evaluates a steady lattice specialization against historical field measurements of sulfur dioxide.

[Run results](f_evaluate/output/RESULTS.md) contains the default run’s estimates. Figures are available as PNG and PDF in the corresponding task outputs.

## Run on macOS or Linux

Extract with a ZIP tool that preserves relative symlinks. The commands below start from the directory containing the ZIP. Python 3.12 was used for the supplied run.

```bash
unzip -q PDP_Gaussian_Plume_CA.zip
cd pdp_gaussian_plume_ca
python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
ipython --quick -c "get_ipython().safe_execfile_ipy('run_pipeline.ipynb', raise_exceptions=True)"
```

The same entry point works from a Jupyter kernel using the project environment. Open `run_pipeline.ipynb` at the project root and run all cells. The runner starts each task in its own `src/` directory and stops on the first error. Raw observations are bundled, so the pipeline needs no network access after package installation. Edit `shared/config.json` before running to change the experiment settings. The default seed is 63.

| Task | Inputs | Main outputs |
| --- | --- | --- |
| `a_import` | `data/prairie_grass`, shared configuration | Observations, release metadata, wind profiles, source hashes |
| `b_benchmark` | Imported configuration | Analytic comparisons, convergence table, time and crosswind profiles |
| `c_coast` | Imported configuration | Forcing, carbon ledger, state snapshots, ablation figures |
| `d_prepare` | Imported observations, releases, and wind profiles | Evaluation cohort, receptor coordinates, grouped folds |
| `e_field` | Prepared field inputs | Out-of-fold predictions, fit parameters, flux ledgers, refinement samples |
| `f_evaluate` | Benchmark, coastal, and field outputs | Results summary, metrics, paired intervals, receptor and peak figures |

Each lettered task has `input/`, `output/`, and `src/`. Relative symlinks in the input directories point to the producing stage. The model notebooks contain code cells only. CSVs are written with headers and units in field names where applicable. The coastal NPZ records scenario, time, and species labels alongside arrays indexed by scenario, time, x, y, z, and species. Surface and stored pools omit the z and species axes.

## 1. Gaussian benchmark

A site stores mass. In free air, one synchronous move has offsets in `{-1, 0, +1}³`. For cell width $h_i$, velocity $u_i$, diffusivity $K_i$, and time step $\Delta t$, define $m_i=u_i\Delta t/h_i$ and $s_i=2K_i\Delta t/h_i^2+m_i^2$. The three probabilities on axis $i$ are $(s_i-m_i)/2$, $1-s_i$, and $(s_i+m_i)/2$. Their product gives the full Moore transition, including the stay state. The displacement has mean $u_i\Delta t$ and variance $2K_i\Delta t$. The chosen grids and time steps keep the probabilities nonnegative. At the ground, a downward move stays in the first vertical cell. Mass crossing the other domain faces leaves.

In a homogeneous unbounded lattice, a puff is the distribution of a sum of independent increments. The Gaussian appears in the many-step, centered and scaled limit. Here the lattice is refined at fixed physical times, with time steps proportional to squared cell width. The analytic comparator uses Gaussian puff probabilities integrated over each cell, with an image source below the ground. The code applies the factored one-dimensional operators, which compute the same homogeneous three-dimensional update. No particle sampling is needed.

Continuous emission integrates that puff kernel over release ages. The finite-time solution approaches the steady advection–diffusion solution with longitudinal diffusion. Dropping longitudinal diffusion gives the classical steady plume with $\sigma_y^2=2K_y x/U$ and $\sigma_z^2=2K_z x/U$ for $x>0$. The notebook measures the classical approximation’s error separately across Péclet numbers $Ux/K_x$.

## 2. Coastal carbon model

The 6.4 × 3.0 km transect contains a ridge and saddle, a rural area, a suburb, an urban area with buildings, and an ocean. The wind and source schedules vary over 150 simulated minutes. Airborne carbon is carried as CO₂-C, volatile organic carbon, or aerosol carbon. The model follows an excess-carbon perturbation above a zero initial state.

- Solid cells block transport. A diagonal path that intersects a blocked face or edge returns to its origin. The prescribed spatially varying wind acts on air cells. Source heights are specified above the local surface.
- A light-modulated first-order reaction transfers volatile organic carbon to aerosol carbon. Its rate and the source schedules are illustrative.
- A first-order surface flux moves CO₂-C and aerosol-C from the lowest exposed cell to a land or ocean pool. Material in each surface pool can return as CO₂-C or transfer to long-lived storage.
- The budget tracks emitted carbon, airborne species, land and ocean pools, storage, and boundary export at every step. The ablations remove solids, replace the wind with its time mean, replace emissions with their time means, disable surface exchange, or disable the reaction. All runs receive the same cumulative carbon input.

The toy model demonstrates process coupling, conservation, and sensitivity. Wind is prescribed kinematically. Aerosol production and surface exchange are effective rates for the demonstration. Quantitative coastal prediction would require a resolved or measured flow and independently estimated rates.

## 3. Prairie Grass field evaluation

Project Prairie Grass released non-buoyant SO₂ over flat terrain near O’Neill, Nebraska, in 1956. Ten-minute samples were collected at 1.5 m on arcs at 50, 100, 200, 400, and 800 m. At 100 m, six towers sampled nine heights from 0.5 to 17.5 m. The field test uses the 44 releases with the EPA evaluation archive’s meteorological metadata. This dataset supplies known release rates and heights, sampler coordinates, surface wind, wind-direction variability, and independent vertical wind profiles. [Experiment and digitized observations](https://harmo.org/jsirwin/PrairieGrassDiscussion.html) · [EPA evaluation](https://nepis.epa.gov/Exe/ZyPURL.cgi?Dockey=P1018OBN.txt)

### Measurements and preparation

- Polar coordinates are bearings clockwise from north. Meteorological wind-from directions are rotated 180° to downwind bearings. A receptor’s distance along the mean flow is its projection onto that bearing. Each model predicts zero on the upwind side under its steady downwind assumption.
- The parser keeps archived receptor records inside the specified integration index range. One receptor outside that range occurs in run 10. An archive value of `-9` is missing and a tower value of zero denotes no measurable concentration. Only recorded receptors are evaluated. The horizontal archive largely contains positive observations, so receptor metrics are conditional on those recorded locations. Arc maxima use the same sampled positions for predictions and observations.
- The recorded concentration unit is mg SO₂/m³. For example, the corrected run 7 maximum at 50 m is 92.91 mg/m³, close to the EPA normalized concentration multiplied by 89.9 g/s and converted from g to mg. Table 5.4 evaporation factors are applied to horizontal samples where a factor is available. Tower values are retained as digitized. The correction file’s unusual 0.09 entry for run 12 is outside the EPA subset.
- Release rates use the polar headers. The original release table confirms 98.9 g/s for run 43, while `PG.DAT` lists 98.6. The EPA profile dates and the receptor archive agree on August 27 for runs 61 and 62. Those dates are used for joining and grouping even though `PG.DAT` labels them August 26. The original receptor sampling windows and the EPA date and hour columns are kept separately.

### Baselines, lattice, and calibration

The nominal Gaussian uses the rural Briggs width curves and the reported stability class. A fitted version estimates a global lateral width multiplier, a global vertical width multiplier, and one additive wind-bearing offset. The wind-variability Gaussian uses the same vertical formula and a lateral width equal to the quadrature sum of 35% of the Briggs width and $x\sigma_\theta$, where $\sigma_\theta$ is the observed directional standard deviation in radians. It gets its own three fitted parameters. Bounds and all constants are in the configuration. The wind-variability closure is a proxy for 10-minute lateral spreading. The implementation also evaluates the curves below 100 m for the closest receptors and for transport from the source. [Briggs parameterization, Table 4.5](https://digital.library.unt.edu/ark:/67531/metadc1090801/m2/1/high_res_d/5591108.pdf)

The field model is the steady, directed specialization of local lattice transport. It advances mass flux through successive x planes with nearest-neighbor jumps in y and z. These hops use a subset of the Moore neighborhood. The continuous-distance jump generators integrate many local hops per output step. The lattice uses a uniform crosswind spacing per run and a vertically stretched grid with a fine surface layer. The crosswind width is at least the configured base spacing and can grow for very wide plumes. The same dispersion closure gives the transverse diffusivities $K_i(x)=(U_2/2)d\sigma_i^2/dx$. This construction makes the flat-wind, reflecting lattice directly comparable to its matched Gaussian.

For shear, the measured tower speeds are interpolated in log height, held at the measured endpoints outside the profile, and normalized to the reported 2 m reference speed. For a cell with vertical thickness $\Delta z_j$, the concentration is flux divided by $U_j\Delta y\Delta z_j$. Adjacent vertical cells exchange tracer in proportion to their concentration gradient, with reflecting ground and open lateral and upper edges. A dry deposition flux of $v_d C$ acts on the surface cell. The standard sensitivity uses $v_d=0.005$ m/s and the higher sensitivity uses 0.010 m/s. These are plausible scenarios for short grass, with no site-specific fit. Transverse jump and sink propagators are composed with symmetric splitting. The numerical checks compare a refined grid, check receptor-wise sink monotonicity, and close the per-run flux budget. [SO₂ dry deposition measurements and rates](https://ww2.arb.ca.gov/sites/default/files/classic/research/apr/past/a6-061-87c_v2.pdf)

The five folds hold out whole meteorological dates. Calibration uses arc concentrations on the other four folds and minimizes day-balanced squared errors of $\log(1+C/C_0)$ with $C_0=1$ mg/m³. Each fit starts from several fixed initial values. Tower concentrations never enter calibration. Each lattice ablation inherits its matched Gaussian’s fitted dispersion and direction, so shear and deposition change with no extra fit. The nominal Briggs comparator is included for context.

The primary empirical score is day-weighted RMSE in $\log(1+C/C_0)$ at individual arc receptors. Within each date the weighting is equal across runs, then arcs, then receptors. Secondary targets are the maximum across observed positions on each arc and tower concentrations by height and bearing. FAC2 is the fraction of positive observations with predictions between one-half and twice the observed concentration. Fractional bias is $2(\bar C_\mathrm{pred}-\bar C_\mathrm{obs})/(\bar C_\mathrm{pred}+\bar C_\mathrm{obs})$, using the same day weights. Percentile intervals resample paired dates with the out-of-fold fits fixed.

### Scope

The field study tests averaged passive-tracer dispersion over flat terrain. Measurements provide receptor concentration and meteorology. The modeled surface sink is a sensitivity and has no independent deposition-flux target here. The field solver assumes downwind advection, a fixed mean bearing per run, and steady conditions. It omits release startup, longitudinal diffusion, and chemical loss. The tower and arc scores describe this historical cohort and do not directly validate the coastal geometry or reaction. Briggs curves incorporate historical dispersion experiments, so the held-out grouping applies to the fitted multipliers and bearing offset for this application.

## Raw sources

- Barad, M. L., ed. (1958), *Project Prairie Grass, A Field Program in Diffusion*, Vol. I. John S. Irwin’s digitization supplies `PGARCS.txt`, `PGVertConc.txt`, `PGrassTABLE_5_4.TXT`, and `PGrassTTUU.txt`. [Archive index](https://harmo.org/jsirwin/PrairieGrassDiscussion.html) · [Polar file format](https://harmo.org/jsirwin/D6589_UGDesign2_Table_2.pdf) · [Original release-rate table](https://harmo.org/jsirwin/PGrassTable5_1.xls)
- U.S. EPA SCRAM’s Prairie Grass evaluation database supplies `AERMET/PG.DAT` and `AERMET/pgrprof.222`. The bundled copies retain the original filenames. [EPA archive](https://gaftp.epa.gov/AIR/aqmg/SCRAM/models/preferred/aermod/eval_databases/pgrass.zip)
