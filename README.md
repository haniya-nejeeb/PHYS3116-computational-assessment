# PHYS3116 Computational Assessment: The Faber-Jackson Relation in SAMI

**Option 2: The Faber-Jackson Relation in the SAMI Galaxy Survey (Data Release 3)**

Team: Haniya Nejeeb, Deagan Marchant

## Research questions

1. **Sample selection:** Which SAMI DR3 galaxies are suitable for measuring the Faber-Jackson (FJ) relation, and why? We keep a record of every galaxy removed and the reason.
2. **The relation:** What is the slope of the FJ relation (L ∝ σ^n) for SAMI early-type galaxies?
3. **Literature comparison:** How does our fit compare to other published fits, and why might it differ?
4. **Evolution of galaxies:** What does this tell us about how different types of galaxies form and evolve?

## Data

Reformatted SAMI DR3 tables from Moodle, in `data/`:

| File | Contents |
|---|---|
| `InputCatGAMADR3.csv` | SAMI galaxies in the GAMA regions (field/group): position, redshift, magnitudes, size, stellar mass |
| `samiDR3InputCatClusters.csv` | SAMI galaxies in the 8 cluster regions: the same as above plus cluster membership |
| `samiDR3StelKin.csv` | Stellar kinematics: velocity dispersion σ, spin parameter λ_R, V/σ |
| `samiDR3VisualMorphology.csv` | Visual morphological type (E, S0, spiral, ...) |
| `*_schema.csv` | Column descriptions for each table |

## Repository layout

```
data/              raw SAMI DR3 csv tables
data/processed/    merged table, selection log, final samples and fit results
notebooks/         analysis notebooks (see notebooks/README.md)
figures/           all saved figures
docs/              data curation and results/discussion write-ups
meetings/          weekly meeting agenda, notes, attendance and action items
results/           outputs of Deagan's original standalone notebook (kept for the record)
```

## Notebooks (run in this order)

| Notebook | What it does |
|---|---|
| `01_load_and_merge.ipynb` | Combines the GAMA and Cluster input catalogues with the kinematics and morphology tables, keeping one cube per galaxy (3,068 galaxies) |
| `02_sample_selection.ipynb` | Applies the quality cuts one at a time and logs why each galaxy was removed, giving 768 early types and 1,109 spirals |
| `03_fj_fitting.ipynb` | Fits the FJ relation (luminosity and stellar-mass forms), compares fit directions and morphological types, and compares with the literature |
| `04_extensions.ipynb` | Tests what changes the slope: dispersion range and selection bias, environment, slow vs fast rotators |
| `SAMI_Extra_Investigations.ipynb` | Aperture comparison, virial size illustration, mass-scale sensitivity and residuals |

## Main results

- 768 early-type galaxies: **L ∝ σ^1.88±0.05** (forward fit) to **σ^2.84±0.07** (inverse fit), below the classic n ≈ 4.
- The relation is steeper for high-σ galaxies and slow rotators, and cluster early types are fainter at fixed σ but have the same stellar mass (higher mass-to-light ratio).
- Full write-up: `docs/results_discussion.md`. 
- Sample selection: `docs/data_curation.md`.

## How to run

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
jupyter notebook
```
