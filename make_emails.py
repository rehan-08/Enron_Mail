"""Build emails.csv from the reviewed labels.
Drops rows flagged to drop, removes helper columns, checks rules, prints counts for DATASHEET.md."""
import pandas as pd

lab = pd.read_csv('candidates_labelled.csv', keep_default_na=False)
lab = lab.drop(columns=[c for c in ('suggested_category', 'suggested_note') if c in lab])
sug = pd.read_csv('label_suggestions.csv', keep_default_na=False)

drop = lab['unsure_note'].str.contains('drop', case=False)
print('dropped (flagged):', int(drop.sum()))
print(lab.loc[drop, ['key', 'unsure_note']].to_string())
out = lab[~drop].copy()
out['unsure_note'] = out['unsure_note'].str.strip()

COLS = ['key', 'source', 'subject', 'body', 'from_address', 'to_addresses', 'category', 'unsure_note']
before = len(out)
out = out.drop_duplicates(subset=['subject', 'body', 'from_address', 'to_addresses'])
print('exact duplicates removed in final file:', before - len(out))

assert (out['body'].str.strip() != '').all(), 'empty body'
assert (out['category'] != '').all(), 'missing category'
assert not out['key'].str.contains(r'(?:^|/)(?:sent|sent_items|_sent_mail|_sent)/').any(), 'sent folder'
assert out['key'].is_unique

out[COLS].to_csv('emails.csv', index=False, encoding='utf-8')

m = out.merge(sug, on='key', how='left')
changed = (m['category'] != m['suggested_category']).sum()
print('\nrows:', len(out), '| mailboxes:', out['key'].str.split('/').str[0].nunique())
print('unsure (note filled):', int((out['unsure_note'] != '').sum()))
print('category != first-pass suggestion:', int(changed))
print(out['category'].value_counts().to_string())
