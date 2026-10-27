# Notebooks

Run the notebooks in order, from this folder (`notebooks/` as the working directory), using the environment in `requirements.txt`. Each notebook reads the files saved by the one before it.

| Notebook | Reads | Saves |
|---|---|---|
| `01_load_and_merge.ipynb` | raw tables in `../data/` | `../data/processed/sami_merged.csv` |
| `02_sample_selection.ipynb` | `sami_merged.csv` | `selection_log.csv`, `sample_early_types.csv`, `sample_spirals.csv`, figures 01–03 |
| `03_fj_fitting.ipynb` | `sample_early_types.csv` | `fj_fit_results.csv`, `fj_mass_fit_results.csv`, figures 04–06 |
| `04_extensions.ipynb` | `sample_early_types.csv` | `fj_extension_results.csv`, `fj_environment_results.csv`, figures 07–09 |
| `SAMI_Extra_Investigations.ipynb` | `sample_early_types.csv` | (plots shown in the notebook) |

`Deagan premerge.ipynb` is Deagan's original standalone analysis (E and E/S0 galaxies only, 446 galaxies), written before the two halves of the project were combined. It is kept for the record and saves its outputs to `../results/`. The final analysis uses notebooks 01–04 and the extra investigations notebook.

## Who did what

- **Haniya:** notebooks 01–04 (loading and merging, sample selection, FJ fitting, extensions), documentation.
- **Deagan:** original standalone analysis, the Oh et al. (2020) comparison, aperture comparison, virial and mass-scale illustrations and residual analysis (`SAMI_Extra_Investigations.ipynb`), corrections to notebooks 02 and 03.
