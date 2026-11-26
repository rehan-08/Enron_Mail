# Enron Received-Mail Labels for a Junk-Mail Filter

A labelled set of 603 received emails from 136 Enron mailboxes, for training and testing a junk-mail filter. Each email is labelled as if it arrived at a wealth-management advisor.

## Source
- Kaggle dataset: [wcukierski/enron-email-dataset](https://www.kaggle.com/datasets/wcukierski/enron-email-dataset)
- Original corpus: https://www.cs.cmu.edu/~enron/
- Received mail only (inbox and filing folders). Sent folders (`sent`, `sent_items`, `_sent_mail`) are excluded.

## Files
| File | What it is |
|---|---|
**Deliverables**
| File | What it is |
|---|---|
| `emails.csv` | Final labelled emails, 603 rows (key, source, subject, body, from_address, to_addresses, category, unsure_note) |
| `DATASHEET.md` | How the data was collected, cleaned, sampled and labelled, with counts that match `emails.csv` |
| `enron-mail.ipynb` | Kaggle notebook: pull, clean and sample the emails, one step per cell (Steps 0–13) |

**Working files (audit trail)**
| File | What it is |
|---|---|
| `candidates.csv` | 592 sampled candidates exported by notebook Step 12, before labelling |
| `bounce_topup.csv` | 15 extra bounce candidates exported by notebook Step 13 |
| `label_suggestions.csv` | First-pass label suggestions from Claude Opus 5.5, committed before review |
| `LABEL_SUGGESTION_PROMPT.md` | The model, the exact instructions it followed, and its 3 second-pass changes |
| `candidates_labelled.csv` | All 607 candidates with reviewed labels |
| `make_emails.py` | Builds `emails.csv` from `candidates_labelled.csv`: drops the 4 flagged rows, checks the rules, prints counts |

## Pipeline
1. Kaggle notebook: load, drop sent folders and the owner's own sent mail, clean, then sample, which gives `candidates.csv` + `bounce_topup.csv`.
2. Labels: LLM suggestions in `label_suggestions.csv`, then a review of every row by hand, which gives `candidates_labelled.csv`.
3. `python make_emails.py` gives `emails.csv`.

## Kaggle notebook
Link: https://www.kaggle.com/code/rehanmhate/enron-mail

## Author
Rehan Mhate · Kaggle: rehanmhate
