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
data/          raw SAMI DR3 csv tables
meetings/      weekly meeting agenda, notes, attendance and action items
```

More folders (notebooks, figures, docs) are added as the project progresses.

## How to run

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
jupyter notebook
```
