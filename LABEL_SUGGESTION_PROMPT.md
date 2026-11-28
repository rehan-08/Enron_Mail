# Label suggestions: tool, model and prompt

Suggested labels in `label_suggestions.csv` were produced by **Claude Opus 5.5** (Anthropic, via Claude Code), on request.
The final `category` values in `emails.csv` are the model's labels: the intern changed none of them during review (see DATASHEET.md).

## Method

**Task setup.** Each email gets exactly one label from a closed set of 17 categories, defined in the labelling guide (version 2026-11-10). The model ran over the 592 candidates in `candidates.csv` (notebook Step 12) and, in a second run, over the 15 bounce top-up emails in `bounce_topup.csv` (notebook Step 13). That makes 607 emails in total.

**Input representation.** A small local script turned each email into one compact text record:
`row index | key | From | To | Subject`, followed by the body with all whitespace collapsed to single spaces.
- Header fields were cut to fixed lengths: From to 60 characters, To to 80, Subject to 90.
- The body was cut to a fixed prefix so that each batch fit in the model's context window: 600 characters for rows 0–74, 450 for rows 75–439, and 300 for rows 440–591 and the 15 top-up emails. Quoted replies, forwarded headers and signatures inside that prefix were left in.
- The `picked_from` column (the keyword pool an email was sampled from) was **not** included in the input, so the pool could not act as a shortcut label. The `key` (mailbox/folder/file) was included, and folder names such as `junk` or `calendar` were visible.

**Batching.** 7 batches: rows 0–74, 75–159, 160–249, 250–344, 345–439, 440–591, and the 15 top-up rows. Each batch was labelled in a single pass, in row order.

**Output format and validation.** For each email the model wrote one line: `row index | category | note` (the note is empty when the call is clear). A build script then joined these lines back to the CSV and checked that:
- every row index from 0 to N−1 has exactly one label (no gaps, no duplicates);
- every label is one of the 17 allowed categories.
The result was saved as `label_suggestions.csv` (key, suggested_category, suggested_note).

**Ambiguity and exclusion handling.** When the guide allowed more than one reading, the model still picked one category and wrote the alternative and the reason in `suggested_note`, for example "could be newsletter". Rows that break a dataset rule rather than a labelling rule were marked in the note for removal instead of being labelled away. These were bodies containing only an attachment filename or a MIME parsing error (no body text), and mail written by the mailbox owner (outgoing, not received). `make_emails.py` drops every row whose note says "drop".

## Instructions the model followed, word for word

> For each email in candidates.csv, suggest exactly one category from the guide below, reading the subject, sender, recipients and body (the model saw the first 300 to 600 characters of the body, depending on the batch; quoted text included).
> Label every email as if it arrived in the inbox of an advisor at a wealth-management firm. Treat Enron as the firm: Enron staff are colleagues; outside people are vendors, partners, clients or personal contacts.
> Do not use the keyword pool the email was sampled from (`picked_from`) as the answer; decide from the email itself.
> If unsure, still pick the best category and give a short reason in suggested_note.
>
> Categories (from the guide, version 2026-11-10):
> client_or_customer_conversation: a client or prospect writing to the firm
> colleague_conversation: people inside the firm writing to each other, including the firm's own bulk mail
> vendor_or_partner_conversation: one-to-one mail with a custodian rep, lawyer, accountant or vendor the firm already works with
> personal_conversation: friends and family
> mailing_list_discussion: people writing to each other on a group list
> chain_forward_by_person: a person forwarding something, even junk
> institution_notice: custodian, bank or regulator notices: statements, trade confirmations, transfers, account alerts, tax documents
> workflow_notification: e-signature requests, CRM tasks, file-share alerts, compliance-tool alerts
> calendar_message: meeting invites, updates, cancellations and replies
> auto_reply: out-of-office and other automatic replies
> bounce: delivery failures
> promotion: ads, offers, sales pitches (even one written by a person), webinar and event marketing
> newsletter: newsletters, digests and market commentary from outside organisations
> phishing_scam: anything trying to steal logins or money
> social_notification: LinkedIn, Facebook and similar notifications
> survey_request: automated feedback and survey requests
> other_junk: any other unwanted bulk mail
>
> Tough calls: a person wrote it to the reader -> a conversation category, unless a scam or sales pitch. A cold sales pitch is promotion. A person forwarding anything -> chain_forward_by_person. Outside market commentary -> newsletter. Webinar/event marketing -> promotion; an invite to an actual meeting -> calendar_message. A list announcement or digest from an organisation -> newsletter; people replying on a list -> mailing_list_discussion.

## How the suggestions were used
1. `label_suggestions.csv` (key, suggested_category, suggested_note) was committed before review.
2. The intern looked over the labels between 03:54 and 04:40 on 2026-11-27 and changed none (DATASHEET.md, Labelling).
3. Changed suggestions = rows where `category` != `suggested_category` (counted in the datasheet).

## Second pass by the model (consistency check)
After the first pass, the model ran rule checks (FW: subjects, "Undeliverable" subjects whose body says delivered/relayed, postmaster senders, Enron senders in outside categories) and changed 3 of its own suggestions in `candidates_labelled.csv`:
- skilling-j/deleted_items/515: vendor_or_partner_conversation -> chain_forward_by_person
- stepenovitch-j/deleted_items/32: bounce -> auto_reply (body says message relayed)
- stepenovitch-j/deleted_items/50: bounce -> auto_reply (body says message relayed)
These are model changes, not intern changes; `label_suggestions.csv` keeps the first-pass suggestions.
