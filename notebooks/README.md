# PHYS3116: Faber–Jackson in SAMI

The question is how stellar mass and luminosity relate to stellar velocity dispersion. The notebook works through the data one step at a time, then checks the lecture comparison, galaxy type and measurement aperture.

## Run it

Extract the whole ZIP. Keep `data/`, `notebooks/` and `results/` together. The input filenames match the repository screenshot, without the download-number suffixes.

Open `notebooks/SAMI_Faber_Jackson.ipynb` with **notebooks as the working directory**, restart the kernel and run from the beginning. The supplied notebook has already been executed. The paths `../data/` and `../results/` go up one folder before entering the required directory. A notebook configured to run from the repository root will need its working directory changed to `notebooks/`.

The Python file has the same code and explanations. From the extracted project root, run:

```text
cd notebooks
python SAMI_Faber_Jackson.py
```

Use an existing Python environment with NumPy, Pandas, Matplotlib and SciPy. `requirements.txt` lists them. Both forms expect the `results/` directory to exist, as it does in this package.

## What is included

- `notebooks/SAMI_Faber_Jackson.ipynb`: the analysis, explanations, outputs and five figures.
- `notebooks/SAMI_Faber_Jackson.py`: the same steps as a script.
- `data/`: the four original catalogue CSVs and four schemas, with simpler filenames and unchanged contents.
- `results/selection_counts.csv`: how many rows remain after each selection.
- `results/selected_galaxies.csv`: the main sample with galaxy IDs, observation IDs and measurements.
- `results/aperture_sample.csv`: the common sample for the two aperture fits.
- `results/fit_summary.csv`: the seven fits, sample sizes, slopes, slope errors and intercepts.
- `figures/`: five snapshots from the checked run, useful for discussing results.

Running the analysis updates the notebook outputs and four CSVs. Separate PNG snapshots need updating separately after changes; figure-saving code is outside the analysis because `savefig` was not verified in the supplied tutorials.

## Why it is written this way

The conversions are written separately. Each fit and plot follows the same visible pattern. There are no custom functions, loops that construct reports, or separate tables tracing every rejected observation. The selection counts, saved sample and comments explain what was chosen and why. Repetition makes each step easier to rewrite and explain.

The earlier residual plot, strict-E-only fit, extra audit tables and general result-building loop have been removed. The main sample and retained fits use the same scientific choices. The five plots cover the mass relation, lecture comparison, magnitude relation, morphology comparison and aperture comparison.

The lines are straight, so plotting their predictions at the measured x values is sufficient. This avoids adding code to construct a separate plotting grid. This shortcut is specific to straight lines; it should not be copied blindly for curved models.

## Tutorial methods

| Code used | Supplied example |
|---|---|
| Imports, variables, lists, dictionaries, `print`, `len` | Tutorial 1 and Tutorial 4 |
| `pd.read_csv`, `.columns`, `.head()` | Tutorial 2: Pandas and Markdown |
| `pd.to_numeric(..., errors='coerce')` | Tutorial 2 Harris-data example |
| `np.concatenate`, list repetition, `np.array` | Spotted Python Week 2 |
| `pd.DataFrame`, `pd.merge`, `.to_csv(index=False)` | Tutorial 2 |
| `.value_counts()` | Tutorial 1 solutions |
| `.dropna(subset=...)`, Boolean masks, galaxy-type selections | Tutorial 4 |
| `np.log` and array arithmetic | Spotted Python Weeks 3–4 and Tutorial 4 |
| `stats.linregress`, slope/intercept and their standard errors, `rvalue` | Tutorial 4 linear-curve-fitting example |
| `plt.plot`, colours, markers, labels, legends, transparency | Tutorial plotting examples |
| `plt.subplots(figsize=...)`, `tight_layout`, `show` | Spotted Python Week 4 |
| `plt.gca().invert_yaxis()` | Tutorial 1 and Spotted Python Week 4 |

Some scientific steps apply those operations to this question. Dividing natural logarithms by `np.log(10)` changes the logarithm base. Dividing the negative magnitude slope by 2.5 gives the luminosity exponent. The aperture and flag comparisons repeat the same fitting method on a stated selection. They are explained applications, rather than claims that an identical exercise appears in a tutorial.

Column meanings and morphology codes come from the supplied schemas. The reference equation is taken from the uploaded Week 3 Monday lecture, PDF page 30, and the luminosity summary from page 33. The mass-to-light discussion comes from the uploaded GalaxyML slides. No additional literature source was used.

## What the assessment needs

This follows Option 2 of the 2026 PHYS3116 brief. It combines mass, kinematic and morphology data; records the selection; plots and fits the relationships; compares with the supplied lecture reference; and discusses interpretation and limits. The aperture comparison provides an investigation beyond the brief's suggestions. The brief rewards clear logic and scientific explanation rather than elaborate code.

The code is only one part of the assessment. The brief also requires at least three documented meetings and three weeks of meaningful code/documentation contributions, a roughly 10-minute group video with at least two minutes per visible speaker, and an individual contribution/reflection statement with the required links. Those need to reflect the team's actual work. This package cannot establish those requirements or guarantee a grade.

## Choices to explain

The main sample uses morphology codes 0 and 0.5, positive effective-radius dispersions and errors, usable mass/type/flag values and the working `bad_class == 0` rule. The schema does not define the flag values, so confirm them before treating this as a validated quality selection. A final comparison shows how including all flag codes changes the slope. The repeated-ID counts must be zero before continuing; replacement data with repeats require a documented observation choice.

`mstar` is already logarithmic. The fit is unweighted and does not model errors in both axes or intrinsic scatter. Missing measurements make the sample incomplete. The lecture's reference selection and fitting details are not fully supplied. The B-band historical illustration and r-band fit are different measurements. These limitations remain part of the scientific explanation.

The numerical summary in the notebook describes the supplied run and must be revised after changes.

## Checked run

All 12 code cells executed without warnings. The main sample contains the same 446 galaxies as the earlier analysis, and all seven retained fits reproduce the earlier coefficients. The notebook and script have matching executable code. All five labelled figures were inspected. The eight input CSVs and schemas retain their original contents.
