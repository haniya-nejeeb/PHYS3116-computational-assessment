# Results and Discussion

This document summarises what we found and what it means. The code and figures are in `notebooks/03_fj_fitting.ipynb`, `notebooks/04_extensions.ipynb` and `notebooks/SAMI_Extra_Investigations.ipynb`. The sample is described in `docs/data_curation.md`.

## 1. Method

The Faber-Jackson (FJ) relation says that an early-type galaxy's luminosity scales with its stellar velocity dispersion as L ∝ σⁿ. Faber & Jackson (1976) found n ≈ 4. Because absolute magnitude is M_r = −2.5 log L + constant, the relation becomes a straight line:

M_r = −2.5 n log σ + constant

We fit straight lines with ordinary least squares (`scipy.stats.linregress`) and convert the slope to n = −slope / 2.5. We also fit the stellar-mass form, log σ against log M*.

## 2. Main results (768 early-type galaxies)

| Fit | Result | Literature |
|---|---|---|
| n, forward fit (M_r on log σ) | 1.88 ± 0.05 | ≈ 4 (Faber & Jackson 1976) |
| n, inverse fit (log σ on M_r) | 2.84 ± 0.07 | |
| n, reduced major axis | 2.31 | |
| log σ vs log M* slope | 0.342 ± 0.008 | 0.285 (Oh et al. 2020) |

- There is a strong correlation (r = −0.81): brighter and more massive early types have higher velocity dispersions. This is what we expect if σ traces the depth of the galaxy's gravitational potential, since the virial theorem gives σ² ∝ GM/R.
- Our data have real scatter in both directions, so least squares gives different answers depending on which variable is treated as y. The forward and inverse fits differ by almost a factor of 1.5 in n. Any comparison with published values has to use the same method.
- E (n = 1.93), E/S0 (1.91) and S0 (1.86) galaxies give almost the same exponent. S0s are slightly shallower, consistent with part of their support coming from rotation.
- Our slope (0.342) is steeper than Oh et al. (2020) (0.285), but the two lines cross near the middle of our mass range, so they differ most for low-mass galaxies. Oh et al. selected galaxies by bulge-to-total ratio (B/T > 0.8), not visual morphology, so the samples are not identical.

## 3. Why is our n lower than 4?

| Explanation | Evidence |
|---|---|
| **Fitting direction** | Forward fits give the shallowest slope; our inverse fit gives n = 2.84. Published studies use different fitting directions, so n can only be compared fairly when the method is the same. |
| **The relation curves** | Galaxies above the median σ (150 km/s) give n = 2.08 ± 0.15, those below give 1.54 ± 0.10 (notebook 04). The original FJ sample was mostly bright ellipticals, where the relation is steepest. Fainter ellipticals have long been known to follow a shallower relation (Davies et al. 1983). |
| **Selection effects** | Cutting a sample by magnitude (the y variable) artificially flattens the slope: keeping only M_r < −21.5 gives n = 0.76. Any magnitude-limited sample is affected in the same way. |
| **Band and aperture** | We use r-band magnitudes and σ within one effective radius. Faber & Jackson used B-band magnitudes and central dispersions. Changing to a fixed 3 kpc aperture changes the stellar-mass slope from 0.342 to 0.358 for the same 767 galaxies (extra investigations notebook). |
| **Sample** | Including S0s, and our quality cuts, changes which galaxies are fitted. The S0 slope is the shallowest. |

No single explanation accounts for the whole difference, but together they make an n of about 2–3 reasonable for a sample like SAMI's, which spans a wide mass range.

## 4. Extensions

### Environment (cluster vs GAMA)

- At the same σ, cluster early types are 0.28 mag fainter than GAMA early types (mean residuals +0.15 ± 0.03 and −0.13 ± 0.03 mag).
- In the stellar-mass form the two environments agree to within 0.01 dex.
- So at fixed σ, cluster galaxies have the same stellar mass but give out less light. That means a higher mass-to-light ratio, as expected if cluster galaxies formed their stars earlier and stopped sooner, leaving older, dimmer stellar populations.
- A systematic photometry difference between the two input catalogues could also contribute.
- The forward-fit slopes differ (GAMA 2.15, cluster 1.47), but the cluster sample has lower masses on average, and the slope depends on mass range, so the slopes alone are hard to compare.

### Slow vs fast rotators

- Using the spin parameter λ_R and the boundary from Cappellari (2016), 145 galaxies are slow rotators and 531 are fast rotators.
- Slow rotators follow a steeper relation (n = 2.17 ± 0.09) than fast rotators (n = 1.76 ± 0.05).
- Most slow rotators are classified E; most fast rotators are S0 or E/S0. So a galaxy's kinematics and its visual morphology tell a consistent story.
- Slow rotators are also brighter on average, so part of the difference is the same curvature seen in the σ split.

### Residuals and mass scale (extra investigations notebook)

- The scatter about the stellar-mass relation is 0.091 dex in log σ (about 23% in σ).
- Multiplying every stellar mass by a constant factor (for example, a different initial mass function) shifts the intercept but cannot change the slope. A slope difference from the literature therefore cannot come from a uniform mass offset.

## 5. What this tells us about galaxy evolution

- The FJ relation exists because a galaxy's stellar motions are set by its mass. More massive galaxies have deeper potential wells and faster-moving stars.
- The relation is not one universal power law. It is steeper for the most massive galaxies and for slow rotators, and shallower for lower-mass, rotating galaxies.
- This fits the picture that massive slow rotators were built up by several mergers, which scrambled ordered rotation into random motions, while fast rotators (mostly S0s) had quieter histories and kept a disk.
- Mergers can add mass without increasing σ much. Gas-poor minor mergers in particular mostly make galaxies larger. That can change how L and σ grow together, and helps explain why the relation curves at the high-mass end.
- Environment changes the light but not the mass at fixed σ, which points to differences in star-formation history (when the stars formed and when star formation stopped) rather than differences in dynamics.

## 6. Limitations

- Ordinary least squares ignores measurement errors and assumes all scatter is in one variable. A fit that models errors in both variables plus intrinsic scatter would be more rigorous.
- Galaxies without a measured σ, and faint galaxies generally, are under-represented.
- Cluster galaxies' magnitudes are less certain because their redshifts include large peculiar velocities.
- GAMA and cluster photometry come from different imaging.
- Published relations used different bands, apertures, selections and fitting methods, so exact agreement is not expected.

## 7. Future work

- Fit the Fundamental Plane (adding effective radius as a third variable), which is known to have much less scatter than the FJ relation.
- Use a fitting method that includes errors in both variables and intrinsic scatter.
- Compare stellar population ages between environments directly, to test the mass-to-light explanation.
- Correct cluster distances for peculiar velocities by using the mean cluster redshift.

## References

- Cappellari, M. 2016, "Structure and Kinematics of Early-Type Galaxies from Integral Field Spectroscopy", ARA&A, 54, 597. [arXiv:1602.04267](https://arxiv.org/abs/1602.04267)
- Croom, S. M. et al. 2021, "The SAMI Galaxy Survey: the third and final data release", MNRAS, 505, 991. [doi:10.1093/mnras/stab229](https://doi.org/10.1093/mnras/stab229), [arXiv:2101.12224](https://arxiv.org/abs/2101.12224)
- Davies, R. L., Efstathiou, G., Fall, S. M., Illingworth, G. & Schechter, P. L. 1983, "The Kinematic Properties of Faint Elliptical Galaxies", ApJ, 266, 41. [doi:10.1086/160757](https://doi.org/10.1086/160757)
- Faber, S. M. & Jackson, R. E. 1976, "Velocity Dispersions and Mass-to-Light Ratios for Elliptical Galaxies", ApJ, 204, 668. [ADS](https://ui.adsabs.harvard.edu/abs/1976ApJ...204..668F)
