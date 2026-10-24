# Week 5 Team Meeting

**Date:** Sunday 18 October 2026

**Duration:** 10 minutes

**Format:** Offline

## Attendance

| Name | Present? | Notes |
|---|---|---|
| Haniya Nejeeb | Present | |
| Deagan Marchant | Absent | No communication after sharing repository |

## Agenda

1. Decide on galaxy sample selection cuts
2. Plan work for the next two weeks before the Week 7 deadline

## Notes
- Haniya was not given collaborator access to the repo created by Deagan and no response from him, so a new one was created today. Due to lack of communication, it was found out later that he had not pushed any work into his repo either so currently there are 2 repos with separate work done by team members. Will be comparing the two and collating the work done to use one repo instead after access has been given to Haniya.

- Option 2, the Faber-Jackson relation in SAMI DR3. Research questions are written in the README.

- We use both the GAMA-region and Cluster input catalogues, so that later we can compare environments. The tables are joined on the SAMI galaxy ID `catid`.

- Some galaxies have more than one cube in the kinematics table. We keep the cube with the smallest σ error.

- σ measured, morphology classified, clean photometry (`bad_class = 0`), cluster members only for cluster galaxies, fractional σ error < 10%. The main FJ sample is E, E/S0 and S0 galaxies, and spirals are kept as a comparison sample.

- Python in Jupyter notebooks (pandas, numpy, matplotlib, scipy).

## Action items

| Task | Owner | Due |
|---|---|---|
| Write notebook to load and merge the SAMI tables | Haniya | End of Week 5 |
| Compare both repos and streamline work | Haniya / Deagan | Week 6 |

## Next meeting
Week 6. Agenda: review the selected sample and fitting methods.
