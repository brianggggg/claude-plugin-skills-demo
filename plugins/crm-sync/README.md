# crm-sync

Pull, push, and de-duplicate CRM contacts and deals without leaving a Claude conversation.

## Commands

| Command | Description |
|---|---|
| `/crm-pull` | Fetch contacts or deals matching a filter from the CRM. |
| `/crm-push` | Create or update a CRM record from data in the conversation. |
| `/crm-dedupe` | Find likely duplicate contacts/companies and propose merges. |

## Bundled skills

None — this plugin is command-only. Its commands call out to a CRM connector rather than performing multi-step reasoning.
