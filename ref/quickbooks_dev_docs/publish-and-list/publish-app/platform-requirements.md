# Publishing Requirements and Guidelines

All apps that connect to production QuickBooks Online companies are expected to comply with Intuit's platform requirements and guidelines. This includes both private (i.e., unlisted) apps and apps that want to be listed on the App Store.

Additionally, apps that operate in certain industries must meet additional requirements before going live.

When you request production [credentials](../../get-started/get-client-id-and-client-secret.md) (i.e., client ID and client secret), you will be asked to complete a [self-assessment questionnaire](https://help.developer.intuit.com/s/questionnaire). This helps us better understand what your app does and how it meets our platform requirements.

- If your app appears to meet our baseline requirements, we'll consider it for approval.
- If we have questions about your responses, or if we need you to make changes to your app, we'll let you know.

In addition to these requirements, apps also need to undergo an annual security assessment. This assessment ensures that all apps on our platform continue to keep Intuit customers' data secure.

> **Note**: These requirements are subject to change as we expand our platform. Please check back periodically for more information and updates.

---

## General Requirements

- Apps that use Intuit APIs (whether public or private) need to be relevant and clearly related to QuickBooks, accounting, payments, workflows, finance, and other acceptable uses. Your app must be designed to either:
  - enhance, streamline, or improve your or other QuickBooks customer's experience or
  - facilitate a business process (e.g. syncing QuickBooks data to another service)
- You'll be asked to disclose certain information about your business, such as complaints, lawsuits, or requests from government agencies related to your business activities. This also applies to independent and/or freelance developers.
- If your app is an integration tool for Intuit products (i.e., your app consumes another third party's APIs and passes the data between it and an Intuit product), you'll be asked to describe the integration and share any instructions that you provide to your customers.
- If you are using another platform to build an integration, you'll be asked to provide information about the other platform and share any instructions they provided to you.
- You or any of your representatives (including owners, affiliated parties, associated parties or any beneficiaries) must not:
  - be on any sanctions lists in the countries available in the app store or
  - be located or do business in Belarus, Cuba, Iran, North Korea, Russia, Syria and the regions of Crimea, Zaporizhzhia and Kherson, the Donetsk People's Republic ("DNR") and Luhansk People's Republic ("LNR") in Ukraine.

---

## Authorization & Authentication

To ensure your app is fully integrated with OAuth2.0, we recommend you do the following:

- If available, [use one of our SDKs](../../develop/authentication-and-authorization/oauth-2.0.md) to develop your app. Our SDKs come with a built-in OAuth 2.0 client library and handle many parts of the authorization process for you.
- Make sure the [redirect URIs](../../develop/authentication-and-authorization/set-redirect-uri.md) you've configured are active and functional.
- Always store the latest `refresh_token` value from the most recent API server response. Use it to make requests and obtain new access tokens and refresh tokens.
- Access tokens are valid for 60 minutes. Use the refresh token to get a new one only when the current one expires and not for every API call.
- Use the [discovery document](../../develop/authentication-and-authorization/oauth-openid-discovery-doc.md) to get the latest endpoints for the OAuth2.0 flow.
- There are certain errors that are returned by the server during the authentication and authorization process. Make sure you address these issues before you put your app into production:
  - Errors due to expired access tokens
  - Errors due to expired refresh tokens
  - Invalid grant errors
  - CSRF errors
- Before you go live, try connecting, disconnecting and reconnecting your app from a non-production or sandbox company. This will help catch any errors in your OAuth2.0 setup and prevent production errors.

---

## Data Usage

Protecting customer data is absolutely essential, and integral to being successful on the QuickBooks API Platform. Any misuse of data or breach in privacy could lead to your app losing access to the APIs.

- You must clearly describe the purposes for using any customer data, and get customers' agreement before using their data for those purposes.
- You must state how you use customer data within your app and if one customer's data is shared with another. Any deviation from what was stated will result in your app being audited for non-compliance.
- You must aggregate and anonymize any customer data, and only use it to surface competitive or other forms of insights to customers, if Intuit customer data is shared across customer accounts.
- Your app must comply with any applicable laws related to customer data, including but not limited to the [GDPR](https://gdpr-info.eu/), [CCPA](https://oag.ca.gov/privacy/ccpa), [LGPD](https://iapp.org/resources/article/brazilian-data-protection-law-lgpd-english-translation/) and [PIPEDA](https://www.priv.gc.ca/en/privacy-topics/privacy-laws-in-canada/the-personal-information-protection-and-electronic-documents-act-pipeda/).

---

## API Usage

The following requirements and best practices help everyone maintain our platform for the benefit of our developer community and customers. They also allow us to gather insights so we can make improvements to our platform.

- Reach out to us via [support page](https://help.developer.intuit.com/s/contactsupport) when there are significant functional changes to your app.
- For apps that call our APIs frequently, we may audit and check your app for efficiency, and/or apply additional throttling limits.
- For seasonal apps, or apps that run only during certain times of the year, reach out and let us know your peak periods. This way, we can monitor and customize throttling limits to properly support your app.

Different requirements will apply to your app based on the type of app you are creating and the entities you're accessing. Read on to know the requirements that are applicable to your app.

### Accounting API

If your app uses any of the accounting (and/or reporting) APIs, these requirements apply to you.

- Users can change their version of QuickBooks Online (i.e., Simple Start, Essentials, Plus, Advanced). That means they get access to new features, or lose the ability to use certain ones. Your app should handle instances when a user may or may not have access to a QuickBooks version-specific feature.
- If your app requires multi-currency settings to be enabled, it should be communicated to the customer and you need to test to ensure that it works as expected. Inversely, ensure that your app works well with a company that has multi-currency enabled or inform customers that your app may not function properly if they have the setting enabled.
- If your app deals with sales tax (for QuickBooks Online companies in any region), verify and thoroughly test that any transactions with taxes are accurate. Your app may be audited to ensure that your app does not miscalculate tax amounts or mess up customers' books.
- If you rely on [webhooks](../../develop/webhooks.md) in your app, you need to test the functionality in a sandbox. In addition, your production endpoint URL must be active and functional.
- If you rely solely on [change data capture operations (CDC)](../../learn/explore-the-quickbooks-online-api/change-data-capture.md) operations, we recommend using webhooks instead to monitor all changes. You should only run CDC at limited frequency to catch up on any changes your system may have missed due to availability or server downtime issues.

### Payments API

Any apps that access the [Payments API](https://developer.intuit.com/app/developer/qbpayments/docs/api/resources/all-entities/bankaccounts) are required to follow the payment application data security standard (PA DSS) established by the [Payment Card Industry (PCI)](https://www.pcisecuritystandards.org/). Since these apps typically access sensitive data, the following requirements are enforced and any apps not following these may lose access to the QuickBooks Payments API.

- You must comply with all the security standards outlined by the [Payment Card Industry's guidelines](https://www.pcisecuritystandards.org/).
- Any Payments API transaction data brought into the QuickBooks company must mask the credit card number: it must all be lowercase x except for the last four digits, with no dashes.
- Design your app so it can handle declined, voided, or refunded payments.
- Your app can't store card security code (CVC2, CVV2, etc) data and Track2 data.
- Your app may not automate any part of the merchant application authorization user interface.
- Your app may not request and/or store the user's Intuit ID.
- Your app must encrypt access tokens before storing them.
- Your app can store access tokens in volatile memory only.
- Your app must include a ReCAPTCHA system to help detect and prevent fraudulent transactions.
- Your app must provide the user with a payment receipt for each payment transaction.
- If your app creates or updates [Charge](https://developer.intuit.com/app/developer/qbpayments/docs/api/resources/all-entities/charges) transactions, you must:
  - use [Tokens](https://developer.intuit.com/app/developer/qbpayments/docs/api/resources/all-entities/tokens) for processing payments
  - include the `context.deviceInfo` field and its child attributes in your request.

### Payroll API

If your app uses the Payroll APIs, these requirements apply to you.

- Users can change their version of QuickBooks Online Payroll (i.e., Core, Premium, Elite). That means they get access to new features, or lose the ability to use certain ones. Your app should handle instances when a user may or may not have access to a QuickBooks version-specific feature.
- Your app should be able to handle payroll corrections.
- You must let us know how your app ensures that no applicable legal caps are exceeded.
- If you are a benefits provider, you must let us know how your app handles the migration of existing benefits plans set up by a customer.

---

## Supporting Your App Users

- All apps must at a minimum be operational and available on a twenty-four-hour, seven days a week. This 24/7 requirement should apply 99.95% of the time in any measurable time increment. In the event of outages or issues, your app must notify and provide servicing support to all end users.
- You must provide a way for your customers to reach out to you for support or questions about your app. This can be an FAQ article, phone number, chat interface, or a similar service.
- You must test your app thoroughly before going live in production and ensure that all API errors, including syntax and validation errors, are appropriately handled.

If you need support from the Intuit team to troubleshoot your app, the following can help expedite your support request.

- Capture the value of the `intuit_tid` field from the Intuit API response header.
- Store all error information in logs (including sequence of API calls, error messages in response, etc) so it can be shared with our support team.

---

## Security Review

All apps on our platform will undergo an annual security review. This review ensures that apps continue to keep Intuit customers' data secure. These are some of the things we look for during the review process:

- You must review and ensure your app complies with [our security policies](security-requirements.md).
- You'll be asked to disclose information about any security breaches in the past that required notification to customers or government agencies/authorities.
- Any breach that has occurred in the past must be resolved before you go live with your Intuit integration.
- Any breach that occurs henceforth must be reported immediately via our [support page](https://help.developer.intuit.com/s/contactsupport).
- Any Intuit credentials including customer IDs, app client ID and client secret must be stored securely and not be exposed within your app.

---

## Requirements for Certain Regulated Industries

If your app is in any industry highlighted below, read on to know more about the types of regulated industries that need further review and our baseline requirements for each.

### Lending

Your app is categorized as a lending app if you allow or promise funding to a small business. For example, through lending, invoice purchase or factoring, or cash advance. This category applies regardless of whether you provide the funds or act as a referral agent, marketer, marketplace, or broker.

The following requirements apply to lending apps:

- You must indicate whether your app relates to consumer or business lending (or both).
- You must comply with applicable lending regulations.
- You must be licensed as a broker or lender where required, and describe what licenses you hold.
- If you offer or facilitate loan products that are originated by a bank partner, you must list the partner(s) you work with.
- Your APR rates must be below 36%.
- You do not engage in or offer Pay-day lending.
- You do not charge prepayment penalties.
- You do not use confession of judgment in servicing or collection.

### Payments/Money Movement

Your app is categorized as a payments or money movement app if it automates payment transactions between two individuals. For example, between a merchant and shopper, employer and employee, individual and bill company). The transactions may include processing, verifying, accepting, or declining credit card or ACH transactions, or making tax payments on the individual's behalf.

Any app that connects to the QuickBooks Payments API is also categorized as 'Payments/Money Movement'.

The following requirements apply to payments/money movement apps:

- If your app uses the Intuit platform as a payment processor, your marketing material and product material must disclose that the payment service is provided by Intuit Payments Inc.
- If you use another payments platform, then you must let us know which platform it is.
- If you process payments yourself, you must have either licenses to provide payment services, or agreements with banks or payment processors to provide payment services on your behalf.
- You must describe the types of transactions that your app enables.
- You'll be expected to have a process for managing regulatory compliance and any required agency reporting. For example, in instances of fraud.

### Insurance

Your app is categorized as an insurance app if it offers insurance products or services, either directly or indirectly.

The following requirements apply to insurance apps:

- You must comply with any applicable insurance laws or regulations.
- You must be licensed in states where licensing requirements apply.

### Investment/Financial Planning

Your app is categorized as an investments or financial planning app if you advise on the sale or purchase of securities, or advise, open, fund, or close 401K, IRA, or other retirement plans.

The following requirements apply to investment/financial planning apps:

- You must comply with any applicable laws related to investments and/or financial planning.
- In some cases, you may need to be licensed or registered as a security advisor or broker.

---

## Non-compliance with Requirements

All new apps or apps that are in the development phase will be required to complete the assessment process prior to getting production credentials.

If your app fails to maintain compliance with these requirements once it is live, or fails to remediate any issues found during the assessment, Intuit will assess the risk and take the necessary steps in order to protect customers' data.

Depending on the type of app and the severity of non-compliance, we may take the following actions:

- Your app users will start seeing warning banners notifying them of your app's non-compliance.
- We'll limit your ability to onboard new customers.
- We'll block your app from making any API calls.

We'll provide sufficient communication and notifications to you before we take any of the above actions. All communication will be sent to the email address registered when you created your app.

Take a moment now to review and update your developer profile as needed and subscribe to our emails. If the email address associated with your app is no longer in use, [contact us](https://help.developer.intuit.com/s/contactsupport) so we can update it.

---

*Source: https://developer.intuit.com/app/developer/qbo/docs/go-live/publish-app/platform-requirements*
