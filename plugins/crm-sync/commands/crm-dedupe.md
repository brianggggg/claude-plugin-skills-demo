---
description: Find likely duplicate contacts/companies and propose merges
---

Scan the CRM for likely duplicate contacts or companies, optionally scoped by `$ARGUMENTS` (e.g. a company domain).

1. Pull candidate records sharing an email domain, phone number, or fuzzy-matched name.
2. Score each pair on match confidence.
3. Present pairs above a reasonable confidence threshold with a suggested "keep" record.
4. On confirmation, merge the losing record's activity history into the kept record.
