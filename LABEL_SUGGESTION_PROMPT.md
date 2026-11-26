# Label suggestions: tool, model and prompt

Suggested labels in `label_suggestions.csv` were produced by **Claude Opus 5.5** (Anthropic, via Claude Code), on request.
They are suggestions only. Every final `category` in `emails.csv` was chosen by the intern after reading the email.

## Request (from the intern)
"can you do the labelling"

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
2. The intern read every email and set `category` and `unsure_note` himself.
3. Changed suggestions = rows where `category` != `suggested_category` (counted in the datasheet).
