# Enron Received-Mail Labels for a Junk-Mail Filter

A labelled set of 500+ received emails from the Enron corpus, for training and testing a junk-mail filter. Each email is labelled as if it arrived at a wealth-management advisor.

## Source
- Kaggle dataset: [wcukierski/enron-email-dataset](https://www.kaggle.com/datasets/wcukierski/enron-email-dataset)
- Original corpus: https://www.cs.cmu.edu/~enron/
- Received mail only (inbox and filing folders). Sent folders (`sent`, `sent_items`, `_sent_mail`) are excluded.

## Files
| File | What it is |
|---|---|
| `emails.csv` | Labelled emails (key, source, subject, body, from_address, to_addresses, category, unsure_note) |
| `DATASHEET.md` | How the data was collected, cleaned, sampled and labelled, with counts |
| `*.ipynb` | Kaggle notebook: pull, clean and sample the emails, one step per cell |

## Kaggle notebook
Link: [TBD (public, run with outputs)](https://www.kaggle.com/code/rehanmhate/enron-mail)

## Author
Kaggle: rehanmhate
