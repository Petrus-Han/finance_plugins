# Technical Requirements

Before you can list your app on the QuickBooks App Store, it will be reviewed to ensure it meets the following technical requirements and complies with the Intuit Developer Terms. This is in addition to meeting our technical and marketing requirements.

The review process starts once you submit your app for review on the QuickBooks App Store. This applies whether you're listing in one or more countries.

All apps listed on the QuickBooks App Store must continue to meet these requirements after publication. They're reviewed by Intuit on an annual basis, or more frequently at Intuit's discretion, to ensure that they continue to meet our required technical and security standards.

> **Note**: The average time to complete the technical review is about 20 days from the date it's initiated. Actual time will depend on availability to schedule reviews, the number of issues found, and the speed with which you can remediate any issues.

---

## Section 1: UI Components (SSO & non-SSO apps)

These requirements cover the public-facing parts of your app (i.e., what's shown to QuickBooks users).

### 1.1: Connect to QuickBooks Button

From within your app, the Connect to QuickBooks button should be visible and presented in an area where users manage their accounting software connections, as shown in the examples below. Once a connection is established, this button should be hidden. Put a disconnect button or link in its place.

> **Note**: Your production redirect URI must be a valid SaaS domain. Learn more about initiating the authorization request.

In this example, prior to connecting to your app, the Connect to QuickBooks button is visible:

Once connection is established, the Connect to QuickBooks button is hidden. Now, the disconnect link is visible.

### 1.2: Browser Compatibility

Widgets, buttons, and workflows work in the latest versions of Edge, Firefox, and Chrome browsers.

### 1.3: Logos and Buttons

All Intuit and QuickBooks logos and buttons in your app use the approved and provided images.

### 1.4: Spelling and Capitalization

"Intuit" and "QuickBooks" are spelled properly, capitalized correctly, and aren't abbreviated.

---

## Section 2: QuickBooks Data Connection (SSO & non-SSO apps)

These requirements detail how your app must initiate, maintain, and reestablish connections with QuickBooks.

### 2.1: Successful Data Connections

Only QuickBooks Online API calls are used to move and pass data between your app and QuickBooks Online. This applies to reading and writing data.

- **Reading data from QuickBooks Online**: Data successfully appears in the app.
- **Writing data to QuickBooks Online**: Data successfully appears in QuickBooks Online.

To speed up this portion of your review, submit a support ticket outlining the steps our review team should follow to test this requirement. For example:

- Link to a video explaining how to use your app
- Link to documentation with on support information
- Provide keys needed to install your app (if applicable)
- Provide account credentials to sign in to your app
- Provide step by step guidance on how to test your app's integration with QuickBooks
- Include any additional caveats and tips

### 2.2: Maintaining Connection

Once users connect via OAuth, the connection is maintained until users disconnect the app from their QuickBooks Online company.

Signing out of an app doesn't disconnect a QuickBooks Online company.

Here's a general overview for maintaining the connection:

1. Users create an account in your app and connect it to their QuickBooks Online company.
2. Launch a different browser.
3. Users sign in to your app.
4. Your app opens with the QuickBooks connection maintained.
5. The "Connect to QuickBooks" button is hidden, but data service calls are working.

### 2.3: Disconnecting Users' QuickBooks Online Companies from Your App

Users should be able to disconnect their QuickBooks Online company connection within your app. There is no mandated disconnect button or link you must use. Just ensure your solution properly calls our revoke endpoint.

The button or link label should clearly indicate it will disconnect your app from QuickBooks.

When a user disconnects, you can identify their company by including realmId as a query parameter in the revoke endpoint. For example: `https://myappsite.com/disconnect?realmId=`

---

## Section 3: Sign-in with Intuit Button (OpenID Connect, Intuit SSO only)

> **Note**: This section is only required if you're using Intuit Single Sign-on.

These requirements are for how your app must use OpenID Connect to implement the Sign in with Intuit button.

> **Warning**: Your app must use the OpenID Connect claimed identity, and must not use the OpenID email address, when creating the association between your app's user and Intuit's OpenID in your database. During subsequent sign-ins, your app must match the OpenID claimed identifier sent by Intuit against what you've associated with your user so the user can gain access to your app. Storing and matching OpenID email addresses isn't secure.

> **Warning**: Your app must establish the association between OpenID Connect and your user only after the user has been securely authenticated into your app via a password prompt or otherwise. This ensures your user is explicitly allowing the OpenID association to give access to your app.

### 3.1: Sign in with Intuit Button

The Sign in with Intuit button appears on all app sign-in pages. It should be clear and visible. When selected, the button launches the Intuit Sign-in page. The button should be rendered using either JavaScript or approved graphics.

> **Warning**: Your app must check for the emailVerified field and allow users access to the app only if emailVerified is true. Otherwise, display an error message to the customer and include a link to https://accounts.intuit.com/app/account-manager/security to verify their address.

### 3.2: Handling Unknown Users

For a new unknown user (i.e., one who is connecting to your app for the first time) who selects the Sign in with Intuit button to sign in with your app without executing the OAuth authentication process:

- While signing in, before the OAuth flow is triggered, your app must check for the emailVerified field in the OpenID user profile response and allow users access to the app only if emailVerified is true. Your app should not connect to the QuickBooks app store if the email account is unverified.
- Display an error message to the customer and include a link to https://accounts.intuit.com/app/account-manager/security for the customer to verify their address.

> **Note**: Display an error message before triggering the OAuth flow if you have not verified the email ID. This will satisfy the requirement.

> **Tip**: Have a workflow or wizard to recognize this customer and offer the ability to either use an existing account for your app, or create a new account. Then inform the user that the app isn't connected to their QuickBooks Online company yet. Show them the Connect to QuickBooks button.

Here's a general overview of the process:

1. User selects the Sign in with Intuit button.
2. User enters their user ID and password for an existing Intuit account that is not currently connected to your app.
3. When the user selects Sign In, the Intuit Sign in window appears. Your app shouldn't interfere with or change the OpenID flow.
4. When the user selects the Authorize button, the authorization screen closes. The user is returned to your app in a signed-in state.

### 3.3: Handling Known Users

An existing connected user who selects the Sign in with Intuit button is taken to your app. Data service calls work.

Here's a general overview of the process:

1. User selects the Sign in with Intuit button.
2. User enters their user ID and password for an existing Intuit account that is currently connected to your app.
3. When the user selects Sign In, they go into your app without entering additional sign-in credentials.
4. The Connect to QuickBooks button is hidden and all data service calls work.

> **Important**: If the user already exists in your database, but their Intuit identity hasn't been established (i.e., the two data identities aren't connected), initiate an application session for that user. Do this only after prompting the user to enter their password prior to linking the Intuit identity to their existing account.

---

## Section 4: Interacting with the QuickBooks App Store and the Apps Tab in QuickBooks Online (Intuit SSO only)

These steps explain the different ways users can find and connect to your app.

If your app uses Intuit Single Sign-on, we'll go over ways to design your app experience that allow users to navigate the QuickBooks App Store.

> **Note**: If your app doesn't use Intuit Single Sign-on, skip to Section 5.

### 4.0: Finding and Managing Apps in QuickBooks Online

The user can go to the Apps tab in QuickBooks Online to find apps and manage existing connections.

If a user is signed in, on the My Apps tab in the QuickBooks App Store there are four actions available for managing your app:

- **Launch**: This links to your app's launch URL, as defined by your app's settings.
- **Support**: We set this up for you. No action required.
- **Disconnect**: This links to your app's disconnect URL, as defined by your app's settings.
- **Write a review**: We set this up for you. It lets users quickly write a review for your app.

### 4.1: Free Trials of Apps

On the QuickBooks App Store, new users can sign up for a free trial of your app if they select the Get integration now button.

Requirements for free trial setup:

- Apps automatically provision users' accounts.
- Landing page doesn't prompt to create or enter a password (unless your app isn't implementing Intuit Single Sign-On).
- Landing page doesn't ask for any information that OpenID Connect provides (name, email, realm ID, client ID, client secret) or the QuickBooks Online API provides (company name, address, phone number, and so on).
- Don't ask users to select a plan or enter payment info.
- Don't show the Connect to QuickBooks button - the user is already connected.

### 4.2: Sign in to an App from the QuickBooks App Store

If a user is signed in to the QuickBooks App Store but not your app, they can sign in to your app without being asked for sign-in credentials.

### 4.3: Launch an App from QuickBooks App Store Without Credentials

If the user hasn't signed out of your app or the QuickBooks App Store, your app should be able to launch from the QuickBooks App store without asking for sign-in credentials.

### 4.4: Disconnect an App from the QuickBooks App Store

A user can disconnect your app (and revoke access) from their QuickBooks Online company from the QuickBooks App Store.

When disconnected:
- Your app no longer appears in the My Apps tab of the Apps menu in QuickBooks Online.
- User gets redirected to a disconnect landing page within your app.
- The disconnect landing page is OpenID-enabled.
- OAuth tokens are invalidated. Your app can no longer make data service calls.

In this disconnected state, the Connect to QuickBooks button should reappear and the Disconnect link should be hidden.

> **Note**: If a user has multiple QuickBooks Online companies associated with the same user ID, they're prompted to pick a specific company.

---

## Section 5: Interacting with the QuickBooks App Store (not using Intuit SSO)

This section only applies to apps that don't implement Intuit Single Sign-on.

### 5.1: Learn More Button

Implement the Learn More button in place of the Get integration now button on your app's QuickBooks App Store listing. Selecting the "Learn More" button redirects users to one of your app's webpages.

The URL should lead to a page about your app, including a description of what it does, guides for how to use it, and info about how it integrates with QuickBooks Online.

### 5.2: Launch URL

The launch URL goes directly to your app's sign-in page.

### 5.3: Disconnect an App from the QuickBooks App Store

Users can disconnect your app from the QuickBooks App Store. The Disconnect URL should be a static page that informs the user that the connection between your app and their QuickBooks Online company is terminated, and provides steps for how to reconnect.

---

## Section 6: Connecting Apps to QuickBooks Online Accountant

### 6.1: Supporting Users with Multiple QuickBooks Online Companies

This section only applies if your app is intended for use with QuickBooks Online Accountant.

Your app needs to be set up so it can sync data for users with multiple QuickBooks Online companies. This is sometimes called "Accountant-ready."

> **Tip**: You don't need to have QuickBooks Online Accountant to create and test apps intended for it.

Your app needs to support these scenarios:

- One user can subscribe two or more separate QuickBooks Online companies to your app successfully.
- The multiple companies must belong to the same QuickBooks admin user.
- The user can launch your app from any or all companies.
- The user can disconnect your app from any or all companies.

> **Note**: Your app must support Intuit Single Sign-on for it to appear in Apps tab in QuickBooks Online Accountant.

### 6.2: Providing Lists for Users Showing Their Multiple QuickBooks Online Companies

We recommend you provide a page that shows users all of their active QuickBooks Online companies. This enhances their experience and gives them a convenient way to manage their connections.

- Provide a disconnect button for each company listed so users can easily disconnect them from your app.
- Provide an Add new company button at the bottom of the page so users can connect additional companies if required.

---

## Section 7: Regulated Industry Check

Prior to starting the technical review process, if your app is used in one or more of the following industries, Intuit will perform an additional review. This ensures your app is compliant in that industry:

- Lending
- Insurance
- Investment and financial planning
- Payments and money movement

---

*Source: https://developer.intuit.com/app/developer/qbo/docs/go-live/publish-app/technical-requirements*
