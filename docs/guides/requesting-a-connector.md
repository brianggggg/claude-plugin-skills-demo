# Requesting a Connector for Review

A connector lets Claude read and write directly in an outside system — Salesforce, Jira, a shared drive, an internal database — instead of you copying data in and out by hand. Because a connector touches a live system, every new one goes through a short security and access review before it's turned on for the team.

## 1. Check what's already available

Ask in the team channel or check with your Claude Code admin — the connector you need may already be approved and just needs to be enabled for you.

## 2. Open a request

Open a new issue using the **Connector Request** template:

[:octicons-issue-opened-24: Open a Connector Request](https://github.com/brianggggg/claude-plugin-skills-demo/issues/new?template=connector-request.md){ .md-button .md-button--primary }

## 3. What to include

The template will prompt for this, but having it ready speeds up review:

- **Connector / system** — what you want Claude connected to
- **Scope** — what data or actions it needs (read-only vs. read/write, which objects, tables, or folders)
- **Authentication method** — OAuth, API key, service account, SSO, etc.
- **Requesting team and contact** — who owns this request
- **Business justification** — what it unblocks or saves time on

Vague requests ("connect to our database") take longer to review than specific ones ("read-only access to the `orders` and `customers` tables in the reporting database, to answer ad-hoc questions about order status").

## 4. Review

A short security and access review follows — checking scope, authentication, and what the connector can touch. Reviewers may follow up with questions on the issue before approving.

## 5. What happens next

Once approved, the connector is enabled for the team and you'll be notified on the issue. If you have questions about the process, check the [FAQ](faq.md) or open an issue and tag it `question`.
