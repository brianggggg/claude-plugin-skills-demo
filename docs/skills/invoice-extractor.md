# invoice-extractor

*Skill*

Extracts vendor, invoice number, line items, totals, and due date from an invoice PDF, image, or forwarded email. Use when a user shares an invoice and asks to log, extract, or process it.

## Used by

- [invoice-processor](../plugins/invoice-processor.md)

## Full skill definition

??? note "SKILL.md contents"

    ```markdown
    # Invoice Extractor

    Pull structured data out of an invoice document.

    ## Fields to extract

    - Vendor name and remit-to address
    - Invoice number and invoice date
    - Due date and payment terms
    - Line items: description, quantity, unit price, line total
    - Subtotal, tax, and grand total
    - Purchase order number, if referenced

    ## Process

    1. Read the entire document before extracting — totals at the bottom confirm line-item math.
    2. If the extracted line-item sum doesn't match the stated total, flag the discrepancy rather than silently trusting either number.
    3. Leave a field blank (not guessed) when it isn't present in the source document.
    4. Output the result as a JSON object matching the fields above, followed by a one-line human-readable summary.
    ```

[:octicons-arrow-left-24: Back to Skills catalog](index.md)
