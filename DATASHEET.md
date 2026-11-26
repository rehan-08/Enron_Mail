# Datasheet: [Email dataset] Corporate mail from Enron

Intern: Rehan Mhate (Kaggle: rehanmhate) · Dates: 2026-11-24 to 2026-11-27 · Guide version: 2026-11-10

## Summary
- Emails submitted: 603
- Per category:
  - colleague_conversation: 136
  - newsletter: 58
  - promotion: 55
  - personal_conversation: 54
  - calendar_message: 53
  - workflow_notification: 51
  - chain_forward_by_person: 47
  - auto_reply: 46
  - bounce: 36
  - vendor_or_partner_conversation: 35
  - mailing_list_discussion: 11
  - other_junk: 9
  - institution_notice: 8
  - survey_request: 2
  - social_notification: 1
  - client_or_customer_conversation: 1
  - phishing_scam: 0
- Unsure: 137

## Sources
- Name and link: The Enron Email Dataset, https://www.kaggle.com/datasets/wcukierski/enron-email-dataset (copy of the CMU Enron corpus, https://www.cs.cmu.edu/~enron/)
- Licence: Kaggle page states "Data files © Original Authors". The corpus was made public by FERC during its investigation and is distributed by CMU for research. Only this 603-email sample is shared here.
- Downloaded on: 2026-11-24 (attached as input to the Kaggle notebook) · Version or file name: Version 2, `emails.csv` (1.43 GB)
- Rows available: 517,401 · Rows taken: 603
- How rows were picked (all steps are in the public notebook, https://www.kaggle.com/code/rehanmhate/enron-mail):
  1. Removed sent folders (`sent`, `sent_items`, `_sent_mail`, and a leftover `_sent`): 391,075 received emails left, from 150 mailboxes.
  2. Removed copies of the owner's own sent mail stored in other folders (`all_documents`, `discussion_threads` and so on). The owner's address is any sender that makes up 10% or more of that mailbox's sent folders: 90,045 removed.
  3. Removed empty bodies (0) and exact duplicates (147,593): a clean pool of 153,422 emails.
  4. `deleted_items` was kept on purpose: it holds received mail, and many auto-replies and bounces end up there.
  5. Keyword pools (subject and sender patterns, using the guide's hints "Out of Office", "Undeliverable", "Accepted:", "Invitation:") were used to find rare categories. These were search helpers only, not labels.
  6. Random sample with seed 42 and a cap per mailbox per pool: auto_reply 50, bounce 50, calendar 50, workflow 60, personal 60, external business 120, junk folders 25, random 185. That gave 597 emails.
  7. Language check (langdetect) and attachment-only check: 5 dropped, 592 left.
  8. Bounce top-up: 15 more from a stricter failure filter (notebook Step 13), because many emails in the bounce pool were delivery receipts. That made 607.
  9. 4 more dropped during labelling: 2 had no real body text, and 2 were really outgoing mail from the mailbox owner. Final: 603 emails from 136 mailboxes.

## Written emails (if you wrote any)
- None. All 603 emails come from the Enron corpus.

## Cleaning
- What was removed or changed: headers moved into subject, from_address and to_addresses. `from_address` is `Name <address>`, with the name taken from X-From. `to_addresses` is `Name <address>; ...` when the X-To names match the To addresses one to one, and addresses only otherwise. 13 HTML bodies were converted to plain text with BeautifulSoup. Quoted replies and signatures were kept. Files are UTF-8.
- Duplicates removed: 147,593 in the pool (same sender, subject and body, keeping the first copy; the same email is often stored in inbox, all_documents and deleted_items). The final file was checked again: 0 duplicates.
- Anything else left out, and why: 5 emails whose body was only an attachment filename, 1 bounce whose body was only a MIME parsing error (no body text), 1 email sent by the owner from his personal aol address, and 1 email sent on the owner's behalf to an outside person. No emails were non-English after an eye check of the 6 that langdetect flagged.

## Labelling
- Who labelled, and roughly how many hours: Labels were first suggested by an LLM (see below). I (Rehan Mhate) reviewed every label against the guide, taking about 2 hours (START–END: 2:30 am - 4:30 am).
- Was a tool or LLM used to suggest labels? Yes. Claude Opus 5.5 (Anthropic, via Claude Code) suggested a category and a reason note for every email. The exact instructions are in `LABEL_SUGGESTION_PROMPT.md`, and the first-pass suggestions are in `label_suggestions.csv`, committed before review. The model then ran a rule-based consistency check and changed 3 of its own suggestions (listed in `LABEL_SUGGESTION_PROMPT.md`). Labels changed by the intern during review: 0.
- Most common reasons for "unsure":
  - Subject says "Out of Office" or "Updated:", but a person wrote it (conversation, not auto_reply or calendar).
  - Delivery receipts and "relayed" notices, which are not failures, so auto_reply rather than bounce.
  - Fantasy-league report emails full of ads (newsletter or promotion).
  - Personal purchases and receipts that fit no category well (other_junk or vendor_or_partner).
  - Mass protest form letters to Ken Lay (other_junk).

## Hard cases
- `dean-c/inbox/692`: colleague_conversation. Subject "Out of Office", but a person wrote it to named colleagues; it is not an automatic reply.
- `donoho-l/inbox/56`: chain_forward_by_person. A person forwarded his own out-of-office note ("FW: Out of Office").
- `stepenovitch-j/deleted_items/32`: auto_reply. The subject says "Undeliverable", but the body says the message was relayed, so it is not a delivery failure.
- `lay-k/inbox/211`: promotion. A think-tank event "Invitation:" with online registration is event marketing, not a real meeting.
- `lay-k/deleted_items/882`: other_junk. A mass form letter sent by many members of the public.
- `hodge-j/inbox/344`: client_or_customer_conversation. A prospect asking for a gas supply quote; the only client email found.
- `wolfe-j/all_documents/155`: vendor_or_partner_conversation. An eBay seller writing after an auction the reader won. It has a PayPal link but is a real purchase, not phishing.
- `bass-e/deleted_items/279`: newsletter. A fantasy-league report service email; the ads make it close to promotion.
- `quigley-d/deleted_items/366`: social_notification. A fantasy-league roster notification, the closest match to a social-network alert.

## Known problems
- The category mix is not the corpus's natural mix: rare categories were deliberately oversampled with keyword pools.
- Few or no examples of client_or_customer_conversation (1), social_notification (1) and phishing_scam (0). The 2000–2002 corpus has almost no LinkedIn-style or phishing mail, and Enron was not a wealth-management firm.
- Owner-address removal uses a 10% share of each mailbox's sent folders. One mailbox had no sent folder, and owners writing from personal addresses can slip through (2 were found and dropped by hand).
- The attachment-only check misses filenames with spaces (2 found by hand).
- `to_addresses` names are missing when the X-To list does not match the To list one to one.
- Labels started as LLM suggestions. The reviewer should spot-check the 137 rows that have an `unsure_note`.
- 5 bodies still contain small HTML fragments inside quoted text.
