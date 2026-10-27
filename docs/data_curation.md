# Data Curation: Which Galaxies We Used and Why

This document records how the galaxy sample for the Faber-Jackson (FJ) analysis was built from the SAMI DR3 tables, which galaxies were removed at each step, and why. The code is in `notebooks/01_load_and_merge.ipynb` and `notebooks/02_sample_selection.ipynb`. Every galaxy's outcome is saved in `data/processed/selection_log.csv`.

## 1. Tables used

| Table | What we take from it |
|---|---|
| `InputCatGAMADR3.csv` (5,536 galaxies) | Absolute r-band magnitude `m_r`, stellar mass `mstar`, ellipticity, photometry flag `bad_class` for galaxies in the GAMA regions (field and group environments) |
| `samiDR3InputCatClusters.csv` (1,433 galaxies) | The same quantities for galaxies in the 8 SAMI cluster regions, plus cluster membership `is_mem` |
| `samiDR3StelKin.csv` (3,426 rows) | Velocity dispersion within one effective radius `sigma_re` and its error, 3 kpc dispersion, spin parameter `lambdar_re` |
| `samiDR3VisualMorphology.csv` (3,068 galaxies) | Visual morphological type |

We use both input catalogues. No galaxy appears in both, so stacking them does not double count anything. Keeping both lets us compare environments.

## 2. Merging

- All tables are joined on the SAMI galaxy ID `catid`.
- **Repeat observations:** 358 rows of the kinematics table are extra cubes for galaxies observed more than once. For each galaxy we keep the cube with the smallest `sigma_re_err`. In most repeats only one cube has a measured σ, so this simply keeps the usable one.
- We start from the kinematics table (left join), so every galaxy SAMI has kinematics for is counted, even if it is later removed. This gives 3,068 galaxies.

## 3. Selection cuts

Cuts are applied in this order. Each galaxy is labelled with the first cut it fails.

| # | Cut | Removed | Remaining | Why |
|---|---|---|---|---|
| 0 | Start: all galaxies with SAMI kinematics | | 3,068 | |
| 1 | Missing or invalid σ | 817 | 2,251 | No dispersion means no FJ measurement. SAMI only reports σ where the spectra were good enough to measure it reliably. |
| 2 | Missing or invalid σ error | 0 | 2,251 | Needed for the precision cut below. |
| 3 | No morphology (type −9 "no agreement" or 5 "unknown") | 102 | 2,149 | We cannot tell whether the galaxy is an early type. |
| 4 | Not in either input catalogue | 1 | 2,148 | No magnitude or stellar mass available. |
| 5 | Bad photometry flag (`bad_class ≠ 0`) | 13 | 2,135 | A non-zero flag marks a galaxy with a photometry or classification problem. The schema does not define each code, so we keep only the clean value 0. This removes very few galaxies (13), so the choice barely affects the result. |
| 6 | Cluster catalogue galaxy that is not a cluster member (`is_mem = 0`) | 31 | 2,104 | These galaxies are foreground or background objects, not part of the cluster, so their environment label would be wrong. |
| 7 | Missing `m_r` or `mstar` | 1 | 2,103 | Needed for both forms of the relation. |
| 8 | Fractional σ error ≥ 10% | 226 | 1,877 | Removes noisy measurements that would add scatter. A 10% error in σ is 0.04 dex, a large fraction of the 0.09 dex scatter about the relation. |

**Not needed:** SAMI DR3 only reports σ above 35 km/s, roughly the instrumental resolution, so no extra low-σ cut is required. The smallest value in the data is 35.0 km/s.

## 4. Splitting by morphology

The 1,877 galaxies that pass every cut are split into:

| Sample | Morphology codes | N | Use |
|---|---|---|---|
| **Early types (main FJ sample)** | 0 (E), 0.5 (E/S0), 1 (S0) | **768** (225 E, 215 E/S0, 328 S0) | All FJ fits |
| Spirals | 1.5 to 3 | 1,109 | Comparison only |

S0s are early-type galaxies that are mostly supported by random motions, like ellipticals. Including them roughly doubles the sample, and fitting E, E/S0 and S0 separately (notebook 03) shows whether including them changes the result.

Type 1.5 (S0/early spiral) galaxies already show disk or spiral structure.

Of the 768 early types, 414 are in the GAMA regions and 354 are in clusters. 676 have a measured spin parameter λ_R, which is used for the slow/fast rotator test in notebook 04.

## 5. Known limitations of the sample

- **Distances in clusters.** Absolute magnitudes depend on distances worked out from redshift. In clusters, galaxies move at up to around 1,000 km/s relative to each other, so their redshifts include a large peculiar velocity on top of cosmic expansion. This adds scatter to `m_r` for cluster galaxies.
- **The sample is not complete.** SAMI selected targets from stellar-mass limited samples, and galaxies are removed where σ could not be measured. Low-luminosity early types are therefore under-represented. Notebook 04 shows the FJ slope depends on which part of the luminosity range is fitted.
- **Photometry from two catalogues.** The GAMA and cluster input catalogues were built from different imaging. Small systematic differences between them could look like an environment effect.

## 6. Output files

| File | Contents |
|---|---|
| `data/processed/sami_merged.csv` | All 3,068 galaxies after merging |
| `data/processed/selection_log.csv` | Every galaxy with its `removed_by` reason (or `kept`) |
| `data/processed/sample_early_types.csv` | The 768-galaxy main sample |
| `data/processed/sample_spirals.csv` | The 1,109-galaxy spiral comparison sample |
| `figures/01_cut_flow.png` | Galaxies remaining after each cut |