# Get Started with the API Explorer

> **Source**: https://developer.intuit.com/app/developer/qbo/docs/get-started/get-started-with-the-api-explorer

## Overview

The [API Explorer](https://developer.intuit.com/app/developer/qbo/docs/api/accounting/most-commonly-used/account) is where you'll find references for all QuickBooks Online Accounting API entities. Each API reference contains relevant fields, operations, attributes, and associated values.

It's also an **interactive tool**. If you [sign in with your developer account](https://developer.intuit.com/dashboard), you can use the sample requests to call specific APIs.

---

## Learn How APIs Are Organized in the API Explorer

Each API has a reference with several sections:

- **Description**: A description of the API entity that summarizes how it relates to QuickBooks
- **Sample API Object**: A sample API object with all possible fields and attributes
- **Operation Sections**: A section for each applicable operation (create, query, read, update, etc.)

The **Sample Entity** sections includes all possible fields and values for the API entity. Each operation section has sample code modules you can use for reference.

All the data you need is contained in the reference, including any notes, call-outs, and other points to consider.

> **Tip**: Most accounting and business workflows, such as invoicing, involve multiple API entities that interact with each other in particular ways. Here's [how to use specific entities to build your app around workflows](https://developer.intuit.com/app/developer/qbo/docs/workflows).

---

## Call Any API Entity

When you sign up for a developer account, you automatically [get a sandbox company](https://developer.intuit.com/app/developer/qbo/docs/develop/sandboxes/manage-your-sandboxes) you can use for testing. You can use the sample requests in API Explorer references to make calls and send sample data to your sandbox company.

### Example: Send a Request to the CompanyInfo Entity

1. [Sign in](https://developer.intuit.com/dashboard) to your developer account.
2. Open another browser tab and then [open a sandbox company](https://developer.intuit.com/app/developer/qbo/docs/develop/sandboxes/manage-your-sandboxes). Keep the tab open.
3. In the first tab, go to [the API Explorer](https://developer.intuit.com/app/developer/qbo/docs/api/accounting/all-entities/account).
4. Select one of your sandbox companies from the dropdown menu at the top.
5. Find and select **CompanyInfo** from the left navigation pane.
6. In the **SAMPLE OBJECT** pane on the right, review the complete list of fields and attributes.

### Use the Sample Code to Perform Operations

1. Find the operation you want to explore.
2. In the **Request URL** section to the right, review the header parameters.
3. In the **Request body** section, review the sample request code. For some operations, you will instead see a **Sample Query** or **Enter ID** box.
4. Edit fields and values in the request as needed.
   > **Tip**: The fields and values need to correspond with actual objects in your sandbox company.
5. When you're ready to send the request, select **Try it**.
6. In the **Returns** section, review the server response.

### Understanding Responses

- If you **queried** an entity, you'll see the payload in the response
- If you **perform an update**, the change will be reflected in your open sandbox company

> **Tip**: You can follow these general steps for any entity in the API Explorer. Try calling the [Invoice](https://developer.intuit.com/app/developer/qbo/docs/api/accounting/all-entities/invoice) entity to create a new invoice object, send it, and see it in your sandbox company.

---

## Mercury Integration Notes

For the Mercury-QuickBooks sync plugin:

1. **API Explorer as Reference**: Use the API Explorer to understand the exact field structures for entities like:
   - `Purchase` (for recording Mercury transactions as expenses)
   - `Deposit` (for recording incoming transfers)
   - `Vendor` (for creating/managing payees)
   - `Account` (for mapping to chart of accounts)

2. **Testing Workflow**: Before implementing API calls in code:
   - Test the exact request format in API Explorer
   - Verify response structures
   - Understand required vs optional fields

3. **Sandbox Testing**: Always test with sandbox companies before connecting to production QuickBooks data.
