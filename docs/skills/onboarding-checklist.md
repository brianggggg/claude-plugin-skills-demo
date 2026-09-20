# onboarding-checklist

*Skill*

Builds a role-specific new-hire onboarding checklist (accounts, equipment, training, introductions) grouped by before day one / week one / first 30 days. Use when a user asks to onboard a new hire or generate an onboarding plan.

## Used by

- [hr-onboarding](../plugins/hr-onboarding.md)

## Full skill definition

??? note "SKILL.md contents"

    ```markdown
    # Onboarding Checklist

    Generate a checklist tailored to the new hire's role, not a generic template.

    ## Inputs needed

    - Role/title and team
    - Start date
    - Manager name
    - Whether the role needs elevated system access (finance, prod infra, customer data, etc.)

    ## Process

    1. Start from the standard baseline: laptop/equipment, email + SSO, org-chart intro, benefits enrollment, first 1:1 with manager.
    2. Add role-specific items — e.g. an engineer needs repo/VPN access and a dev environment; a salesperson needs CRM access and territory assignment.
    3. If the role touches sensitive systems, add the corresponding access-request step rather than assuming standard equipment covers it.
    4. Group the output into **before day one**, **week one**, and **first 30 days**, each as a checkbox list.
    5. Flag any input you didn't get (e.g. no manager name) instead of leaving that step vague.
    ```

[:octicons-arrow-left-24: Back to Skills catalog](index.md)
