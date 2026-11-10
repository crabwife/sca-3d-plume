# Gaussian plume and local lattice transport

The same local lattice process is tested under uniform transport and with measured winds or stack conditions. The coastal landscape is a process demonstration. The field cases score observed tracer concentrations and use Gaussian comparators driven by the same inputs.

- **Explore the coast.** Download [the interactive 3D view](i_landscape/output/coastal_3d.html) and open it in a browser. Rotate the ridge and city, select the carbon species and scenario, and scrub or play 150 minutes of simulated transport. The viewer runs offline. [Animation](i_landscape/output/coastal_3d.mp4) · [Still](i_landscape/output/coastal_3d.png)
- **Compare field predictions.** [Prairie Grass wind and calibration ablations](g_alignment/output/metrics.csv) · [Kincaid stack tracer scores](h_kincaid/output/metrics.csv) · [Original benchmark and field results](f_evaluate/output/RESULTS.md)

### Field results from the supplied run

| Field case and lattice variant | Individual arc receptors | Arc peaks | Tower receptors |
| --- | ---: | ---: | ---: |
| Prairie Grass, prior flat-wind lattice | 1.647 | 1.318 | 1.470 |
| Prairie Grass, original report's source wind, joint fit | 1.057 | 0.827 | 0.647 |
| Prairie Grass, two wind stations, joint fit | 1.023 | 0.807 | 0.621 |
| Prairie Grass, two wind stations, separate fit | 1.128 | 0.533 | 0.645 |
| Kincaid, physical stack height | — | 1.258 | — |
| Kincaid, stack height plus buoyant rise | — | 0.431 | — |

Scores are day-weighted RMSE of $\log(1+C/C_0)$. Prairie Grass uses $C_0=1$ mg/m³ and holds out whole release days. Kincaid uses $C_0=1$ µg/m³ with physical inputs fixed before scoring. The cases use distinct concentration scales and measurement designs.

At Prairie Grass, using the source wind from the original report produced most of the gain. For the joint fit, adding the second station changed arc-receptor RMSE by −0.034 with a paired day-bootstrap interval of [−0.068, −0.003]. The separate fit improved sampled peaks further with higher individual arc error. At Kincaid, buoyant rise reduced the overprediction from the physical stack-height case. The rise case still tended to underpredict and its day-weighted factor-of-two score was 0.134. The matched Gaussian and lattice agree closely in both cases.

## Run on macOS or Linux

Clone the repository with Git to preserve relative symlinks. The supplied run used Python 3.12.

```bash
git clone https://github.com/crabwife/sca-3d-plume.git
cd sca-3d-plume
python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
ipython --quick -c "get_ipython().safe_execfile_ipy('run_pipeline.ipynb', raise_exceptions=True)"
```

The same entry point works from a Jupyter kernel using the project environment. Open `run_pipeline.ipynb` at the project root and run all cells. The runner starts each task in its own `src/` directory and stops on the first error. The first Kincaid import downloads the EPA input archive and checks its SHA-256. For an offline run after installing dependencies, place the archive specified in the source manifest at `data/kincaid/kinsf6.zip`. Edit `shared/config.json` before running to change the experiment settings. The default seed is 63.

| Task | Inputs | Main outputs |
| --- | --- | --- |
| `a_import` | Archived field inputs, shared configuration | Observations, release metadata, wind profiles, source hashes |
| `b_benchmark` | Imported configuration | Analytic comparisons, convergence table, time and crosswind profiles |
| `c_coast` | Imported configuration | Forcing, carbon ledger, state snapshots, ablation figures |
| `d_prepare` | Imported observations, releases, and wind profiles | Evaluation cohort, receptor coordinates, grouped folds |
| `e_field` | Prepared field inputs | Out-of-fold predictions, fit parameters, flux ledgers, refinement samples |
| `f_evaluate` | Benchmark, coastal, and original field outputs | Results summary, metrics, paired intervals, receptor and peak figures |
| `g_alignment` | Prepared Prairie Grass data, original predictions, two-station winds | Held-out wind and calibration ablations |
| `h_kincaid` | Imported Kincaid arc maxima and stack weather | Quality-screened arc-peak scores, matched Gaussian and lattice |
| `i_landscape` | Coastal demo frames and ledgers | Rotatable HTML, MP4 animation, still image |

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
- The budget tracks emitted carbon, airborne species, land and ocean pools, storage, and boundary export at every step. The ablations remove solids, replace the wind with its time mean, replace emissions with their time means, disable surface exchange, or disable the reaction. All original coastal ablations receive the same cumulative carbon input.

The toy model demonstrates process coupling, conservation, and sensitivity. Wind is prescribed kinematically. Aerosol production and surface exchange are effective rates for the demonstration. Quantitative coastal prediction would require a resolved or measured flow and independently estimated rates.

### Interactive landscape

The demonstration adds a sea-breeze component to the prescribed wind. Its streamfunction gives a landward near-surface contribution, rising motion on the land side, and a return contribution aloft. The heated-land run also has stronger vertical mixing over developed cells. Aerosol has a small settling velocity and a surface deposition rule. Windward and rural CO₂ sources and suburban and city emission patches are prescribed. City VOCs react into aerosol through the original light-modulated conversion. Rates and circulation strength are illustrative. [Sea-breeze circulation](https://www.noaa.gov/jetstream/ocean/sea-breeze)

A separate initial stock of solid CaCO₃ carbon erodes on the lee slope. Nearest-neighbor runoff moves it along a river to the marine sediment pool. Atmospheric and mineral carbon have separate ledgers. The whole budget includes both emitted carbon and the initial rock stock. At the default setting, all four scenarios use the same city emission pulses and rock input. The interactive view shows full terrain, flattened terrain, suppressed thermal circulation, and suppressed air–surface exchange. Source heights follow the surface in the flat scenario. Colors mark sampled concentrations with a fixed scale within each species. Vertical exaggeration makes the terrain and buildings visible.

The full-resolution demonstration frames are a generated intermediate. The supplied [frame ledger](c_coast/output/demo_ledger.csv) samples the budget at ten-minute intervals, and the simulator checks conservation every 12 seconds.

## 3. Prairie Grass field evaluation

Project Prairie Grass released non-buoyant SO₂ over flat terrain near O’Neill, Nebraska, in 1956. Ten-minute samples were collected at 1.5 m on arcs at 50, 100, 200, 400, and 800 m. At 100 m, six towers sampled nine heights from 0.5 to 17.5 m. The field test uses the 44 releases with the EPA evaluation archive’s meteorological metadata. This dataset supplies known release rates and heights, sampler coordinates, surface wind, wind-direction variability, and independent vertical wind profiles. [Experiment and digitized observations](https://harmo.org/jsirwin/PrairieGrassDiscussion.html) · [EPA evaluation](https://nepis.epa.gov/Exe/ZyPURL.cgi?Dockey=P1018OBN.txt)

### Measurements and preparation

- Polar coordinates are bearings clockwise from north. Meteorological wind-from directions are rotated 180° to downwind bearings. A receptor’s distance along the mean flow is its projection onto that bearing. Each model predicts zero on the upwind side under its steady downwind assumption.
- The parser keeps archived receptor records inside the specified integration index range. One receptor outside that range occurs in run 10. An archive value of `-9` is missing and a tower value of zero denotes no measurable concentration. Only recorded receptors are evaluated. The horizontal archive largely contains positive observations, so receptor metrics are conditional on those recorded locations. Arc maxima use the same sampled positions for predictions and observations.
- The recorded concentration unit is mg SO₂/m³. For example, the corrected run 7 maximum at 50 m is 92.91 mg/m³, close to the EPA normalized concentration multiplied by 89.9 g/s and converted from g to mg. Table 5.4 evaporation factors are applied to horizontal samples where a factor is available. Tower values are retained as digitized. The correction file’s unusual 0.09 entry for run 12 is outside the EPA subset.
- Release rates use the polar headers. The original release table confirms 98.9 g/s for run 43, while `PG.DAT` lists 98.6. The EPA profile dates and the receptor archive agree on August 27 for runs 61 and 62. Those dates are used for joining and grouping even though `PG.DAT` labels them August 26. The original receptor sampling windows and the EPA date and hour columns are kept separately.

### Original comparison of shear and dry deposition

The nominal Gaussian uses the rural Briggs width curves and the reported stability class. A fitted version estimates a global lateral width multiplier, a global vertical width multiplier, and one additive wind-bearing offset. The wind-variability Gaussian uses the same vertical formula and a lateral width equal to the quadrature sum of 35% of the Briggs width and $x\sigma_\theta$, where $\sigma_\theta$ is the observed directional standard deviation in radians. It gets its own three fitted parameters. Bounds and all constants are in the configuration. The wind-variability closure is a proxy for 10-minute lateral spreading. The implementation also evaluates the curves below 100 m for the closest receptors and for transport from the source. [Briggs parameterization, Table 4.5](https://digital.library.unt.edu/ark:/67531/metadc1090801/m2/1/high_res_d/5591108.pdf)

The field model is the steady, directed specialization of local lattice transport. It advances mass flux through successive x planes with nearest-neighbor jumps in y and z. These hops use a subset of the Moore neighborhood. The continuous-distance jump generators integrate many local hops per output step. The lattice uses a uniform crosswind spacing per run and a vertically stretched grid with a fine surface layer. The crosswind width is at least the configured base spacing and can grow for very wide plumes. The same dispersion closure gives the transverse diffusivities $K_i(x)=(U_2/2)d\sigma_i^2/dx$. This construction makes the flat-wind, reflecting lattice directly comparable to its matched Gaussian.

For shear, the measured tower speeds are interpolated in log height, held at the measured endpoints outside the profile, and normalized to the reported 2 m reference speed. For a cell with vertical thickness $\Delta z_j$, the concentration is flux divided by $U_j\Delta y\Delta z_j$. Adjacent vertical cells exchange tracer in proportion to their concentration gradient, with reflecting ground and open lateral and upper edges. A dry deposition flux of $v_d C$ acts on the surface cell. The standard sensitivity uses $v_d=0.005$ m/s and the higher sensitivity uses 0.010 m/s. These are plausible scenarios for short grass, with no site-specific fit. Transverse jump and sink propagators are composed with symmetric splitting. The numerical checks compare a refined grid, check receptor-wise sink monotonicity, and close the per-run flux budget. [SO₂ dry deposition measurements and rates](https://ww2.arb.ca.gov/sites/default/files/classic/research/apr/past/a6-061-87c_v2.pdf)

The five folds hold out whole meteorological dates. Calibration uses arc concentrations on the other four folds and minimizes day-balanced squared errors of $\log(1+C/C_0)$ with $C_0=1$ mg/m³. Each fit starts from several fixed initial values. Tower concentrations never enter calibration. Each lattice ablation inherits its matched Gaussian’s fitted dispersion and direction, so shear and deposition change with no extra fit. The nominal Briggs comparator is included for context.

The primary empirical score is day-weighted RMSE in $\log(1+C/C_0)$ at individual arc receptors. Within each date the weighting is equal across runs, then arcs, then receptors. Secondary targets are the maximum across observed positions on each arc and tower concentrations by height and bearing. FAC2 is the fraction of positive observations with predictions between one-half and twice the observed concentration. Fractional bias is $2(\bar C_\mathrm{pred}-\bar C_\mathrm{obs})/(\bar C_\mathrm{pred}+\bar C_\mathrm{obs})$, using the same day weights. Percentile intervals resample paired dates with the out-of-fold fits fixed.

### Scope

The field study tests averaged passive-tracer dispersion over flat terrain. Measurements provide receptor concentration and meteorology. The modeled surface sink is a sensitivity and has no independent deposition-flux target here. The field solver assumes downwind advection, a fixed mean bearing per run, and steady conditions. It omits release startup, longitudinal diffusion, and chemical loss. The tower and arc scores describe this historical cohort and do not directly validate the coastal geometry or reaction. Briggs curves incorporate historical dispersion experiments, so the held-out grouping applies to the fitted multipliers and bearing offset for this application.

### Measured wind alignment

The two-station comparison uses the 10-minute mean vectors transcribed from Table 6.1 in the original report. The stations were 2 m above ground, one 25 m west of the release and the other 450 m north and 30 m west of the source. The downwind sampling window was delayed using a travel-time estimate. The importer subtracts the report's approximate 8° vane correction. Run 29 falls back to the source station. The transcription retains the two partial-record flags and printed page numbers. This is a reconstruction conditional on the available winds. [Table 6.1, pp. 209–214](https://harmo.org/jsirwin/PGrassVol1Chap6.pdf)

Wind components interpolate along the projected downwind coordinate. The plume centerline advances with slope $v/u$, then follows the final vector beyond the second station. In the moving cross-section, tracer jumps to its nearest neighbors in $y$ and $z$. Independent Poisson hop counts give the exact transition kernel on each axis. An image about the ground face enforces reflection, and total flux divided by the local streamwise wind gives concentration. The paired Gaussian uses the same drift, variance, source, and boundary. These are steady, flat-wind cross-sections. The original comparison above retains the independent shear and dry-deposition tests.

Both wind inputs are crossed with both calibration choices on the original five release-day folds. Joint calibration fits the receptor loss. Separate calibration fits the lateral width from centered arc profiles, a bearing offset from their centroids, and vertical dilution from crosswind-integrated concentrations. Those moments use training arcs that sample both sides of the core. Tower observations enter scoring only. Per-target tables include sampled peak bearing error and paired day intervals conditional on the fitted parameters. This follow-up uses the historical cohort already examined during development.

## 4. Kincaid power-plant tracer

The 1980–1981 Kincaid experiment injected SF₆ into the exhaust of a 187 m stack. The second case uses hourly arc maxima in the Model Validation Kit and hourly stack temperature, exit speed, tracer rate, and meteorology from the EPA input archive. The Kit supplies concentrations in µg/m³ and sampling quality flags. It converts the original mixing ratios with pressure and temperature. For example, on April 20, 1980, hour 14, the Kit reports 0.748 µg/m³ at 3 km where the EPA summary displays 127 under a mass-concentration heading. [Field experiment](https://harmo.org/jsirwin/KincaidHourlyDiscussion.html) · [Validation Kit guide, Tables 2 and 4](https://www.harmo.org/Kit/Download/Kit_UsersGuide.pdf)

The supplied cohort comprises 300 arc-hours from 24 days. It uses the 3–10 km nominal arcs, quality 2 or 3, neutral or unstable stability classes, positive warm-stack emissions, and stations beyond the calculated terminal-rise distance. At each radius the model evaluates the plume centerline at ground level, corresponding to the target measured by the arc maximum. The time-series inputs use the archive's reference wind near 100 m. The score is weighted equally by day, then hour, then available arc. FAC2 uses positive measured peaks and the same hierarchical weighting.

The two variants inject tracer at stack height or at stack height plus a buoyancy-dominated Briggs terminal rise. Both use the same reflecting lattice and dispersion widths. Each has a matched Gaussian control. The 3–10 km restriction keeps the Briggs width formula within its stated downwind range. Observed mixing heights are retained with predictions for diagnosis. The experiment uses steady, vertically uniform transport and a single effective source height. Bootstrap resampling is by campaign date. [EPA evaluation archive](https://www.epa.gov/scram/air-quality-dispersion-modeling-preferred-and-recommended-models) · [Briggs rise equations](https://gaftp.epa.gov/aqmg/SCRAM/models/other/isc3/isc3v2.pdf)

## Raw sources

- Barad, M. L., ed. (1958), *Project Prairie Grass, A Field Program in Diffusion*, Vol. I. John S. Irwin’s digitization supplies `PGARCS.txt`, `PGVertConc.txt`, `PGrassTABLE_5_4.TXT`, and `PGrassTTUU.txt`. [Archive index](https://harmo.org/jsirwin/PrairieGrassDiscussion.html) · [Polar file format](https://harmo.org/jsirwin/D6589_UGDesign2_Table_2.pdf) · [Original release-rate table](https://harmo.org/jsirwin/PGrassTable5_1.xls)
- U.S. EPA SCRAM’s Prairie Grass evaluation database supplies `AERMET/PG.DAT` and `AERMET/pgrprof.222`. The bundled copies retain the original filenames. [EPA archive](https://gaftp.epa.gov/AIR/aqmg/SCRAM/models/preferred/aermod/eval_databases/pgrass.zip)
- The Kincaid source manifest records the EPA archive and the Model Validation Kit copies of `SF6_KIN.DAT` and `MET_K1.DAT`. [Source manifest](data/kincaid/source.json) · [Validation Kit download](https://www.harmo.org/kit_download.php)
