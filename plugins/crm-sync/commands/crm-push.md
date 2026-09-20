---
description: Create or update a CRM record from data in the conversation
---

Create or update a CRM record using the details in `$ARGUMENTS` or the preceding conversation.

1. Identify whether this is a new contact/deal or an update to an existing one (match by email or deal ID).
2. Map the available fields onto the CRM schema.
3. Confirm the diff with the user before writing.
4. Push the change and report the resulting record ID.
