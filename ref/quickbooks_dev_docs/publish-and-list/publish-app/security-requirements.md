# Security Requirements

Before you can [list your app on the QuickBooks App Store](../list-on-the-app-store.md), it will be reviewed to ensure it meets the following security requirements and complies with the [Intuit Developer Terms](https://developer.intuit.com/app/developer/qbo/docs/legal-agreements/intuit-terms-of-service-for-intuit-developer-services). This is in addition to meeting our technical and marketing requirements.

The security review starts [once your app passes the technical review](technical-requirements.md).

Following the initial security review, developers must remediate any critical, high or medium priority issues before they can be published on the app store. For ongoing compliance reviews, these issues should be fixed within 2 weeks of notification by Intuit.

Apps listed on the QuickBooks App Store must continue to meet these requirements after publication. All apps listed on the app store, and any app with over 500 connections, will be [reviewed by Intuit on an annual basis](../list-on-the-app-store/maintaining-compliance.md), or more frequently at Intuit's discretion, to ensure they continue to meet our required technical and security standards.

> **Note**: The average time it takes for an app to complete its initial security review is about 7 days. This can vary depending on the issues found during the review process.

---

## App Server Configuration

Ensure your server configuration meets the following requirements:

- Caching is disabled on all SSL pages and all pages that contain sensitive data by using value `no-cache` and `no-store` instead of `private` in the Cache-Control header.
- All OS, web-server, and app-server security patches are up to date, and that new patches are applied in a commercially reasonable timeframe after they are made available by the hardware and software vendors.
- SSL must be configured to support TLS version 1.1 or higher. TLS version 1.2 using AES 256 or higher with SHA-256 is recommended.
- HTTPS is enforced on all pages of your app.
- The app web server must be configured to disable the TRACE and other HTTP methods if not being used.
- You must not log any user's credentials or QuickBooks data.

---

## Attack Vulnerability

During the security test, Intuit will ensure that your app is secure against the following vulnerabilities. Test accordingly and resolve any issues prior to submitting your app for review:

- Cross Site Request Forgery
- Cross Site Scripting (including reflected and stored cross site scripting)
- SQL Injection
- XML Injection
- Authentication, Sessions Management and functional level access control (if any)
- Forwards or redirects in use have been validated

---

## QuickBooks Data Usage

These tests verify that your app meets Intuit's requirements for handling QuickBooks data:

- Your app does not provide third-parties with access to a customer's QuickBooks data, via external API calls or any other means.
- Your app cannot export, save, or store QuickBooks data for any purpose other than the functional use of your app.

---

## Cookie Management

Verify that all app session cookies have the following attributes set:

- Secure
- HTTPOnly

---

## OAuth Token Management

Verify that your app meets these requirements for OAuth 2.0 token management:

- Intuit OAuth tokens or customer-identifying information is not exposed within your app or shared with other parties.

Once a user completes the OAuth authorization workflow:

- Encrypt and store the refresh token and realmID in persistent memory.
- Encrypt the refresh token with a symmetric algorithm (3DES or AES). AES is preferred.
- Store your AES key in your app, in a separate configuration file.

In addition to the above requirements, refer to these best practices for [handling OAuth 2.0 tokens](../../develop/authentication-and-authorization/oauth-2.0.md#token-storage-best-practices) within your app.

---

## Sensitive Information

Web application endpoints that receive sensitive customer information and/or authentication tokens in URL parameters must not return HTML content via an HTTP Response Body. This is to prevent sensitive customer information from being accidentally leaked to 3rd parties in the subsequent HTTP Referer request headers.

Instead, the web application endpoints should implement a 302 Found redirect. This is particularly important when application end points are handling authentication tokens.

---

## User Credentials

Your storage of user credentials (e.g., username, password, account numbers, etc.), must comply with [Intuit's Password Policy](https://developer.intuit.com/app/developer/qbo/docs/legal-agreements/password-policy-for-intuit-developer-services). Only developers with prior written approval from Intuit may store user credentials used to access end user data from another source (e.g., the end user's financial institution).

In the event we expressly allow you to store user credentials locally within your Developer Application, ensure that:

1. The account ID is unique for that end user
2. The password is a minimum of 8 characters in length
3. 128-bit SSL is used when transferring any password or Account ID over the internet
4. The password is not stored in plain text and is one-way hashed via SHA-256 (or better) and stored only as hashed values

---

## Security Scans and Audits

Consistent with our [Intuit Developer Terms](https://developer.intuit.com/app/developer/qbo/docs/legal-agreements/intuit-terms-of-service-for-intuit-developer-services), you are required to:

- Allow us to conduct system vulnerability scans within two (2) weeks of our request, or provide access to reputable scan results*, provided the scan was conducted within the last year;
- Complete a security affidavit within two (2) weeks of our request; and
- Promptly take action to remediate any issues identified by system vulnerability scans and app reviews.

*Intuit reserves the right to question or reject scan results that an app provides. If that occurs, you must either allow us to conduct the scans described above, or conduct a new scan sufficient to show compliance with our Intuit Developer Terms.

---

*Source: https://developer.intuit.com/app/developer/qbo/docs/go-live/publish-app/security-requirements*
