# %% [markdown]
# # PHYS3116: Faber–Jackson in SAMI
#
# I want to see how stellar mass and luminosity relate to the spread of stellar velocities in SAMI galaxies. I start with E and E/S0 galaxies, compare the fitted relationships with the lecture, then check spirals and a different measurement aperture.
#
# The steps are written out in order, using the supplied tutorial methods. Run from the first cell with **`notebooks/` as the working directory**. `../data/` and `../results/` refer to the folders one level above it. The README maps the methods to the tutorials.
#
# This is Option 2 of the **2026 PHYS3116 brief**. The separately supplied 2025 PHYS2116 brief is a different project.

# %% [markdown]
# ## 1) Load the four tables
#
# First I need the input properties, the stellar motions and the galaxy types. I print the columns so I can check their names before using them.
#
# *Tutorial 2: reading and inspecting tables; Tutorial 4: imports.*

# %%
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats

gama = pd.read_csv('../data/InputCatGAMADR3.csv')
clusters = pd.read_csv('../data/samiDR3InputCatClusters.csv')
kinematics = pd.read_csv('../data/samiDR3StelKin.csv')
morphology = pd.read_csv('../data/samiDR3VisualMorphology.csv')

print('GAMA rows:', len(gama))
print('Cluster rows:', len(clusters))
print('Kinematic observations:', len(kinematics))
print('Morphology rows:', len(morphology))
print(gama.columns)
print(kinematics.columns)
print(morphology.head())

# %% [markdown]
# ## 2) Get the numbers ready
#
# `catid` identifies a galaxy and `cubeidpub` identifies an observation. `mstar` is already $\log_{10}(M_\star/M_\odot)$, while `m_r` is absolute r-band magnitude.
#
# `sigma_re` is the velocity dispersion within the Sérsic effective-radius aperture, in km/s. Its matching error is `sigma_re_err`. The `sigma_3kpc_round` columns describe the fixed 3 kpc aperture used later.
#
# I convert the columns explicitly. `errors='coerce'` turns unreadable entries into `NaN`; it does not turn them into zero.
#
# *Tutorial 2: `pd.to_numeric`.*

# %%
# Keep the conversions separate so I can see which columns are being used.
gama['catid'] = pd.to_numeric(gama['catid'], errors='coerce')
gama['mstar'] = pd.to_numeric(gama['mstar'], errors='coerce')
gama['m_r'] = pd.to_numeric(gama['m_r'], errors='coerce')
gama['bad_class'] = pd.to_numeric(gama['bad_class'], errors='coerce')

clusters['catid'] = pd.to_numeric(clusters['catid'], errors='coerce')
clusters['mstar'] = pd.to_numeric(clusters['mstar'], errors='coerce')
clusters['m_r'] = pd.to_numeric(clusters['m_r'], errors='coerce')
clusters['bad_class'] = pd.to_numeric(clusters['bad_class'], errors='coerce')

kinematics['catid'] = pd.to_numeric(kinematics['catid'], errors='coerce')
kinematics['sigma_re'] = pd.to_numeric(kinematics['sigma_re'], errors='coerce')
kinematics['sigma_re_err'] = pd.to_numeric(kinematics['sigma_re_err'], errors='coerce')
kinematics['sigma_3kpc_round'] = pd.to_numeric(kinematics['sigma_3kpc_round'], errors='coerce')
kinematics['sigma_3kpc_round_err'] = pd.to_numeric(kinematics['sigma_3kpc_round_err'], errors='coerce')

morphology['catid'] = pd.to_numeric(morphology['catid'], errors='coerce')
morphology['type'] = pd.to_numeric(morphology['type'], errors='coerce')

# %% [markdown]
# ## 3) Put the input catalogues together
#
# GAMA and the cluster catalogue supply different sets of galaxies. I stack matching columns and put them into one table. The source label records the catalogue; it does not establish cluster membership.
#
# *Spotted Python Week 2: `np.concatenate` and lists; Tutorial 2: `pd.DataFrame`.*

# %%
input_data = pd.DataFrame({
    'catid': np.concatenate((gama['catid'], clusters['catid'])),
    'mstar': np.concatenate((gama['mstar'], clusters['mstar'])),
    'm_r': np.concatenate((gama['m_r'], clusters['m_r'])),
    'bad_class': np.concatenate((gama['bad_class'], clusters['bad_class'])),
    'catalogue': np.concatenate((['GAMA'] * len(gama), ['Cluster catalogue'] * len(clusters)))
})
input_data = input_data.dropna(subset=['catid'])

# A repeated ID could create extra rows when the tables are merged.
input_counts = input_data['catid'].value_counts()
morphology_counts = morphology['catid'].value_counts()
print('Repeated input IDs:', len(input_counts[input_counts > 1]))
print('Repeated morphology IDs:', len(morphology_counts[morphology_counts > 1]))

# %% [markdown]
# ## 4) Check the dispersion measurements
#
# I remove missing dispersions and errors, then require both to be positive. This is a basic numerical check, not a complete survey-quality definition. Some galaxies have repeated observations, so I count the remaining IDs before merging.
#
# **The three repeated-ID checks in Sections 3–4 must give zero before continuing.** They do for the supplied data. If new data give repeats, stop and resolve them first. The code does not automatically choose an observation.
#
# *Tutorial 4: `dropna` and masks; Tutorial 1 solutions: `value_counts`.*

# %%
kin_present = kinematics.dropna(subset=['catid', 'sigma_re', 'sigma_re_err'])
kin_good = kin_present[(kin_present['sigma_re'] > 0) & (kin_present['sigma_re_err'] > 0)]

kin_counts = kin_good['catid'].value_counts()
print('Observations with the required measurements:', len(kin_present))
print('Observations with positive dispersion and error:', len(kin_good))
print('Repeated usable galaxy IDs:', len(kin_counts[kin_counts > 1]))

# Keep the observation ID so I can trace each measurement later.
kin_table = pd.DataFrame({
    'catid': kin_good['catid'],
    'cubeidpub': kin_good['cubeidpub'],
    'sigma_re': kin_good['sigma_re'],
    'sigma_re_err': kin_good['sigma_re_err'],
    'sigma_3kpc_round': kin_good['sigma_3kpc_round'],
    'sigma_3kpc_round_err': kin_good['sigma_3kpc_round_err']
})
type_table = pd.DataFrame({'catid': morphology['catid'], 'type': morphology['type']})

# %% [markdown]
# ## 5) Match the galaxies and choose the sample
#
# The inner merges keep shared `catid` values. I then remove rows missing mass, morphology or flag information. Since `mstar` is logarithmic, `mstar > 0` is just a broad check for a mass above one solar mass; these supplied masses already pass it.
#
# The main sample uses **E = 0 and E/S0 = 0.5**. E/S0 is transitional. Exact categories avoid accidentally including the no-agreement code −9 with `type < 1`.
#
# I retain `bad_class == 0` as a **working rule** from the earlier analysis. The schema does not define the individual codes, including zero, so this needs confirmation. Section 11 checks its numerical effect. `aper_corr_flag` concerns corrections to $V/\sigma$ and $\lambda_R$ and is not used to select dispersion measurements.
#
# *Tutorial 2: merging; Tutorial 4: galaxy selection.*

# %%
matched_input = pd.merge(kin_table, input_data, on='catid')
matched = pd.merge(matched_input, type_table, on='catid')
complete = matched.dropna(subset=['mstar', 'type', 'bad_class'])
mass_data = complete[complete['mstar'] > 0]
zero_flags = mass_data[mass_data['bad_class'] == 0]

ellipticals = zero_flags[(zero_flags['type'] == 0) | (zero_flags['type'] == 0.5)]
spirals = zero_flags[(zero_flags['type'] >= 2) & (zero_flags['type'] <= 3)]

print('Rows after the input match:', len(matched_input))
print('Rows after the morphology match:', len(matched))
print('E and E/S0 galaxies:', len(ellipticals))
print('Spiral galaxies:', len(spirals))
print(ellipticals['type'].value_counts())

# Write the counts out in the same order as the selection above.
selection_counts = pd.DataFrame({
    'step': ['Original observations', 'Required measurements present',
             'Positive dispersion and error', 'Matched input catalogue',
             'Matched morphology', 'Mass, type and flag present',
             'Positive logarithmic mass', 'Zero bad_class', 'E and E/S0'],
    'rows': [len(kinematics), len(kin_present), len(kin_good), len(matched_input),
             len(matched), len(complete), len(mass_data), len(zero_flags), len(ellipticals)]
})
print(selection_counts)

# %% [markdown]
# ## 6) Fit stellar mass against dispersion
#
# Now I can look at the relationship. I use
#
# $$x=\log_{10}[\sigma_e/(\mathrm{km\,s^{-1}})],\qquad y=\log_{10}(M_\star/M_\odot),\qquad y=ax+b.$$
#
# `np.log` is a natural logarithm, so I divide by `np.log(10)`. `mstar` is already logged. `stats.linregress` fits the line and reports its slope, intercept and their standard errors.
#
# The fit is unweighted. The reported dispersion errors are kept in the sample table, but are not used as weights or displayed as error bars here. Errors in both axes and intrinsic scatter are outside this fitting method.
#
# *Tutorial 4: linear fitting and plotting; Spotted Python: arrays and logarithms.*

# %%
log_sigma = np.log(np.array(ellipticals['sigma_re'])) / np.log(10)
log_mass = np.array(ellipticals['mstar'])

mass_fit = stats.linregress(log_sigma, log_mass)
mass_line = mass_fit.slope * log_sigma + mass_fit.intercept

print(f'Mass slope: {mass_fit.slope:.3f} +/- {mass_fit.stderr:.3f}')
print(f'Intercept: {mass_fit.intercept:.3f} +/- {mass_fit.intercept_stderr:.3f}')
print(f'Correlation r: {mass_fit.rvalue:.3f}')

# These are straight lines, so the measured x values are enough to draw them.
fig, ax = plt.subplots(figsize=(8, 5))
plt.plot(log_sigma, log_mass, 'x', alpha=0.5, label=f'E and E/S0, N = {len(ellipticals)}')
plt.plot(log_sigma, mass_line, color='red', label=f'Fit: slope = {mass_fit.slope:.3f}')
plt.xlabel(r'$\log_{10}[\sigma_e/(\mathrm{km\,s^{-1}})]$')
plt.ylabel(r'$\log_{10}(M_\star/M_\odot)$')
plt.title('Stellar mass and velocity dispersion')
plt.legend()
plt.tight_layout()
plt.show()

# %% [markdown]
# ## 7) Compare with the lecture
#
# The Week 3 Monday lecture, PDF page 30, shows Oh et al. (2020) as
#
# $$\log_{10}\sigma_e=0.285\log_{10}M_\star-0.845,$$
#
# using km/s and solar masses. I fit in that same direction below. Reversing the fitted axes requires a new regression; taking the reciprocal of the earlier slope would give a different result for scattered data.
#
# This compares with the equation **on the supplied slide**. The slide shows a bulge-to-total category that this selection does not reproduce, and gives limited details of the fitting method and reference sample.

# %%
reference_fit = stats.linregress(log_mass, log_sigma)
our_reference_line = reference_fit.slope * log_mass + reference_fit.intercept
lecture_line = 0.285 * log_mass - 0.845

print(f'Our slope: {reference_fit.slope:.3f} +/- {reference_fit.stderr:.3f}')
print('Lecture slope:', 0.285)
print('Difference:', reference_fit.slope - 0.285)

fig, ax = plt.subplots(figsize=(8, 5))
plt.plot(log_mass, log_sigma, 'x', alpha=0.5, label='E and E/S0')
plt.plot(log_mass, our_reference_line, color='red', label='Our fit')
plt.plot(log_mass, lecture_line, '-', color='black', label='Oh et al. (2020), lecture page 30')
plt.xlabel(r'$\log_{10}(M_\star/M_\odot)$')
plt.ylabel(r'$\log_{10}[\sigma_e/(\mathrm{km\,s^{-1}})]$')
plt.title('Comparison with the lecture relation')
plt.legend()
plt.tight_layout()
plt.show()

# %% [markdown]
# ## 8) What about luminosity?
#
# The lecture summary gives $L\propto\sigma^4$. Stellar mass and luminosity differ because the mass-to-light ratio depends on the stellar population. I use the supplied r-band magnitude for a second fit:
#
# $$M_r=c\log_{10}[\sigma_e/(\mathrm{km\,s^{-1}})]+d.$$
#
# The tutorial magnitude relation can be written $M_r=C-2.5\log_{10}L_r$. Combining the two equations gives
#
# $$L_r\propto\sigma_e^{\alpha_r},\qquad \alpha_r=-c/2.5,\qquad s_{\alpha_r}=s_c/2.5.$$
#
# This is algebra applied to the tutorial relation. The catalogue uses r-band magnitude, while the historical illustration on lecture page 30 uses B-band; the comparison is not an exact reproduction of that sample.
#
# *Spotted Python Week 4: magnitudes; Tutorial 4: the same straight-line fit.*

# %%
magnitude_data = ellipticals.dropna(subset=['m_r'])
magnitude_sigma = np.log(np.array(magnitude_data['sigma_re'])) / np.log(10)
magnitude = np.array(magnitude_data['m_r'])

magnitude_fit = stats.linregress(magnitude_sigma, magnitude)
magnitude_line = magnitude_fit.slope * magnitude_sigma + magnitude_fit.intercept
luminosity_exponent = -magnitude_fit.slope / 2.5
luminosity_error = magnitude_fit.stderr / 2.5

print('Galaxies with r-band magnitudes:', len(magnitude_data))
print(f'Magnitude slope: {magnitude_fit.slope:.3f} +/- {magnitude_fit.stderr:.3f}')
print(f'Luminosity exponent: {luminosity_exponent:.3f} +/- {luminosity_error:.3f}')
print('Lecture summary exponent:', 4)

fig, ax = plt.subplots(figsize=(8, 5))
plt.plot(magnitude_sigma, magnitude, 'x', alpha=0.5, label='E and E/S0')
plt.plot(magnitude_sigma, magnitude_line, color='red', label='Magnitude fit')
plt.gca().invert_yaxis()
plt.xlabel(r'$\log_{10}[\sigma_e/(\mathrm{km\,s^{-1}})]$')
plt.ylabel('Absolute r-band magnitude (mag)')
plt.title('Magnitude form of the Faber–Jackson relation')
plt.legend()
plt.tight_layout()
plt.show()

# %% [markdown]
# ## 9) Try the same fit for spirals
#
# I use the spiral sample from Section 5 and repeat the same calculation. This helps compare galaxy types. The ranges of mass and dispersion can also differ, so a difference in slope alone cannot prove a different formation history.
#
# *Tutorial 4: separate galaxy types and repeat the linear fit.*

# %%
spiral_sigma = np.log(np.array(spirals['sigma_re'])) / np.log(10)
spiral_mass = np.array(spirals['mstar'])
spiral_fit = stats.linregress(spiral_sigma, spiral_mass)
spiral_line = spiral_fit.slope * spiral_sigma + spiral_fit.intercept

print(f'E and E/S0 slope: {mass_fit.slope:.3f} +/- {mass_fit.stderr:.3f}')
print(f'Spiral slope: {spiral_fit.slope:.3f} +/- {spiral_fit.stderr:.3f}')

fig, ax = plt.subplots(figsize=(8, 5))
plt.plot(spiral_sigma, spiral_mass, '.', alpha=0.3, color='blue', label=f'Spirals, N = {len(spirals)}')
plt.plot(log_sigma, log_mass, 'x', alpha=0.5, color='red', label=f'E and E/S0, N = {len(ellipticals)}')
plt.plot(spiral_sigma, spiral_line, color='blue', label='Spiral fit')
plt.plot(log_sigma, mass_line, color='red', label='E and E/S0 fit')
plt.xlabel(r'$\log_{10}[\sigma_e/(\mathrm{km\,s^{-1}})]$')
plt.ylabel(r'$\log_{10}(M_\star/M_\odot)$')
plt.title('Does the galaxy type matter?')
plt.legend()
plt.tight_layout()
plt.show()

# %% [markdown]
# ## 10) Same galaxies, different aperture
#
# For the extra investigation, I compare the effective-radius and 3 kpc measurements. I require usable measurements in both, then fit both relations on **the same galaxies and observations**. That keeps the sample consistent while the aperture changes.
#
# The two fits share galaxies, so their separate errors do not give a formal significance test of the difference. This uses the same masks, logarithms and fitting method again.

# %%
both_apertures = ellipticals.dropna(subset=['sigma_3kpc_round', 'sigma_3kpc_round_err'])
both_apertures = both_apertures[(both_apertures['sigma_3kpc_round'] > 0) &
                               (both_apertures['sigma_3kpc_round_err'] > 0)]

both_mass = np.array(both_apertures['mstar'])
re_sigma = np.log(np.array(both_apertures['sigma_re'])) / np.log(10)
kpc_sigma = np.log(np.array(both_apertures['sigma_3kpc_round'])) / np.log(10)

re_fit = stats.linregress(re_sigma, both_mass)
kpc_fit = stats.linregress(kpc_sigma, both_mass)
re_line = re_fit.slope * re_sigma + re_fit.intercept
kpc_line = kpc_fit.slope * kpc_sigma + kpc_fit.intercept

print('Galaxies in both fits:', len(both_apertures))
print(f'Effective-radius slope: {re_fit.slope:.3f} +/- {re_fit.stderr:.3f}')
print(f'3 kpc slope: {kpc_fit.slope:.3f} +/- {kpc_fit.stderr:.3f}')

fig, ax = plt.subplots(figsize=(8, 5))
plt.plot(re_sigma, both_mass, 'x', alpha=0.4, color='red', label='Effective radius')
plt.plot(kpc_sigma, both_mass, '.', alpha=0.4, color='blue', label='3 kpc')
plt.plot(re_sigma, re_line, color='red', label='Effective-radius fit')
plt.plot(kpc_sigma, kpc_line, color='blue', label='3 kpc fit')
plt.xlabel(r'$\log_{10}[\sigma/(\mathrm{km\,s^{-1}})]$')
plt.ylabel(r'$\log_{10}(M_\star/M_\odot)$')
plt.title(f'Aperture comparison: the same {len(both_apertures)} galaxies')
plt.legend()
plt.tight_layout()
plt.show()

# %% [markdown]
# ## 11) Check the flag choice
#
# Since the flag codes were not defined in the supplied schema, I return to the E/E-S0 sample before the zero-flag cut. This checks how much the choice changes the slope. It does not establish which flag codes are scientifically acceptable.

# %%
all_flags = mass_data[(mass_data['type'] == 0) | (mass_data['type'] == 0.5)]
all_sigma = np.log(np.array(all_flags['sigma_re'])) / np.log(10)
all_mass = np.array(all_flags['mstar'])
all_fit = stats.linregress(all_sigma, all_mass)

print('Flag codes before the cut:')
print(all_flags['bad_class'].value_counts())
print(f'All codes: N = {len(all_flags)}, slope = {all_fit.slope:.3f} +/- {all_fit.stderr:.3f}')
print(f'Zero only: N = {len(ellipticals)}, slope = {mass_fit.slope:.3f} +/- {mass_fit.stderr:.3f}')

# %% [markdown]
# ## 12) Save the useful tables
#
# I save the selection counts, selected galaxies and paired aperture sample so the choices can be followed. The fit summary keeps the numerical results together. Galaxy IDs and observation IDs stay in the sample tables.
#
# `../results/` already exists in the supplied folder. `index=False` leaves out an extra Pandas row-index column.
#
# *Tutorial 2: DataFrames and `to_csv`.*

# %%
# The lists follow the same order: main, reference, magnitude, spirals, apertures, flags.
fit_summary = pd.DataFrame({
    'fit': ['Mass on dispersion', 'Dispersion on mass', 'r-band magnitude on dispersion',
            'Spiral mass on dispersion', 'Paired effective radius', 'Paired 3 kpc', 'All flags'],
    'N': [len(ellipticals), len(ellipticals), len(magnitude_data), len(spirals),
          len(both_apertures), len(both_apertures), len(all_flags)],
    'slope': [mass_fit.slope, reference_fit.slope, magnitude_fit.slope, spiral_fit.slope,
              re_fit.slope, kpc_fit.slope, all_fit.slope],
    'slope_error': [mass_fit.stderr, reference_fit.stderr, magnitude_fit.stderr, spiral_fit.stderr,
                    re_fit.stderr, kpc_fit.stderr, all_fit.stderr],
    'intercept': [mass_fit.intercept, reference_fit.intercept, magnitude_fit.intercept,
                  spiral_fit.intercept, re_fit.intercept, kpc_fit.intercept, all_fit.intercept]
})

selection_counts.to_csv('../results/selection_counts.csv', index=False)
ellipticals.to_csv('../results/selected_galaxies.csv', index=False)
both_apertures.to_csv('../results/aperture_sample.csv', index=False)
fit_summary.to_csv('../results/fit_summary.csv', index=False)
print(fit_summary)
print('Saved the tables.')

# %% [markdown]
# ## 13) What I take from this
#
# For the supplied run, there are **446 E/E-S0 galaxies**. The mass-on-dispersion slope is **2.139 ± 0.064**. In the lecture equation's direction, the slope is **0.333 ± 0.010**, compared with 0.285. The r-band luminosity exponent is **1.929 ± 0.066**, compared with the lecture summary's exponent 4.
#
# The spiral mass slope is **3.115 ± 0.073** for **1,053 galaxies**. For the same **446 galaxies**, changing to the 3 kpc aperture gives **2.105 ± 0.059**, compared with **2.139 ± 0.064** at the effective radius. Including all flag codes gives **447 galaxies** and a mass slope of **2.138 ± 0.064**.
#
# More massive galaxies in the main sample tend to have larger stellar velocity dispersions. This is consistent with the lecture's connection between gravity and stellar motions. Galaxy structure and the region measured also matter. The morphology comparison is useful for discussing different dynamical structures, but these fits alone cannot establish how an individual galaxy formed or evolved.
#
# The luminosity result differs from the lecture's simple exponent. The band, sample, mass-to-light ratios and fitting assumptions can all matter; this analysis does not isolate one explanation. The same caution applies to the comparison with the lecture's published mass relation.
#
# The main limitations are the incomplete measurement sample, the unresolved flag definitions, different populations in the morphology comparison, and an unweighted fit that does not handle errors in both axes or intrinsic scatter. The source slide also gives limited information about its reference sample. Small fitted errors do not account for all of those effects.
#
# A next step would be to confirm the catalogue flags and inspect unusual objects in the saved sample. These statements and numbers need updating if the data or selection changes.
