---
description: Fetch contacts or deals matching a filter from the CRM
---

Fetch CRM records matching the filter given in `$ARGUMENTS` (e.g. `stage:negotiation owner:me`).

1. Parse the filter into CRM query parameters.
2. Call the CRM connector's search endpoint.
3. Present results as a table with name, stage, owner, and last-activity date.
