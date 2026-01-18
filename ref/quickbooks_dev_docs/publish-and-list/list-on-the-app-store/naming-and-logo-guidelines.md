# App name, logo, and advertising restrictions

## App name and company name guidelines

Your app is required to comply with our trademark and branding guidelines, as described in the [Intuit Developer Terms](https://developer.intuit.com/app/developer/qbo/docs/legal-agreements/intuit-terms-of-service-for-intuit-developer-services). This means, among other things:

- You are prohibited from using any Intuit brand or brand element in the title of your application, your app card or your other branding.
- You are permitted to make truthful, factual references to Intuit's products and services in plain-text descriptions of the features and benefits of your app.
- You cannot use "QuickBooks," "QB," "QBO," "QBOA," "ProAdvisor," "Intuit," "Turbo", "ProAdvisor," "Mint" or any other Intuit brand (the "Intuit Brands") or brand elements (e.g. "quick," "intui," or "tuit"), including phonetic equivalents (e.g. "qwik" or "QuBee"), in the name or branding of your business, application, service, business source identifiers or any other programs and/or materials.
- You cannot use special characters like `<`, `>`, `\`, `"` for your app name.
- Your logos cannot be a mimicked version, similar to or an alteration of an Intuit Brand logo; nor, can your logos contain any Intuit Brands, brand elements or Intuit logos.
- Your business name and/or logo must be clearly displayed at the top of your website.
- Your business name and/or logo must appear larger than any Intuit Brand or Intuit Brand logo (used only as set forth above), including but not limited to authorized logos you display on your website, under the Intuit Developer Program Agreement.

## "Connect to QuickBooks" button

Implement your own on-click method with one of the buttons below to invoke the location in your app that initiates the [OAuth 2.0 workflow](/app/developer/qbo/docs/develop/authentication-and-authorization/oauth-2.0). Define classes for both base and hover states.

- Display this button to users who have not authorized access, yet. That is, not connected to a QuickBooks company.
- Include this button on any page in your app.
- Do not modify the appearance of any button graphics.
- After the connection is established, replace the button with a way for users to disconnect: a button or link titled "Disconnect from QuickBooks." When clicked, it invokes the location in your app that [revokes access](/app/developer/qbo/docs/develop/authentication-and-authorization/oauth-2.0#revoke-token-disconnect).

The user clicks the "Connect to QuickBooks" button you provide in your app to initiate the authorization workflow for a QuickBooks company.

This button corresponds to these [scopes](/app/developer/qbo/docs/learn/scopes):

- `com.intuit.quickbooks.accounting` - The QuickBooks Online Accounting API
- `com.intuit.quickbooks.payment` - The QuickBooks Payments API

During the authorization workflow, the user selects a company and then authorizes your app to access the data. After the user authorizes the connection, the browser is redirected back to your app. Learn more about [authorization](/app/developer/qbo/docs/develop/authentication-and-authorization/oauth-2.0).

### "Connect to QuickBooks" button graphics

[Download the Connect to QuickBooks button images](https://static.developer.intuit.com/resources/Connect_to_QuickBooks_buttons.zip).

This .zip file includes "Connect to QuickBooks" graphics in png and svg format, both base and hover states. These buttons are available in English and French.

### "Connect to QuickBooks" button usage guidelines

**Color**
- Use one of the green buttons is preferred.
- Use a transparent button when there is not enough contrast with the page background to use a green button.

**Size**
- Use the button size as is.

**Aspect ratio**
- Maintain the same aspect ratio as the original.

### "Connect to QuickBooks" buttons (English)

[Image: C2QB_composite_English.svg]

### "Connect to QuickBooks" buttons (French)

[Image: C2QB_composite_French.svg]

## "Sign in with Intuit" button

Implement your own on-click method with one of the buttons below to invoke the location in your app that initiates the [OpenID Connect](/app/developer/qbo/docs/develop/authentication-and-authorization/openid-connect) authentication workflow. Define classes for both base and hover states.

- Place this button anywhere on a page, display it only for users not already signed in.
- Preserve the appearance or behavior of any graphics you use directly.
- Don't use a link or another widget to start the sign in process.

If you're implementing [modified single sign-on](/app/developer/qbo/docs/develop/authentication-and-authorization/single-sign-on-models), adding this button, and associated implementation, is optional.

The user clicks the "Sign in with Intuit" button you provide in your app to initiate the Intuit Single Sign-on authentication workflow.

This button corresponds to these [scopes](/app/developer/qbo/docs/learn/scopes):

- `openid` - OpenID Connect processing
- `profile` - User's given and family names
- `email` - User's email address
- `phone` - User's phone number
- `address` - User's physical address

During the authentication workflow, the user is prompted to log in with their Intuit user ID (email) and password. After user authentication is complete, the browser is redirected back to your app. [Learn more about Intuit Single Sign-on](/app/developer/qbo/docs/develop/authentication-and-authorization/single-sign-on-models).

### "Sign in with Intuit" button graphics

[Download Sign in with Intuit button images](https://static.developer.intuit.com/resources/Sign_in_with_Intuit_buttons.zip).

This .zip file includes "Sign in with Intuit" graphics in png and svg format, both base and hover states.

### "Sign in with Intuit" button usage guidelines

**Color**
- Use one of the blue buttons is preferred. Use a transparent button when there is not enough contrast with the page background to use a blue button.

**Size**
- Use the button size as is.

**Aspect ratio**
- Maintain the same aspect ratio as the original.

### "Sign in with Intuit" buttons (English)

[Image: SIWI_composite_English.svg]

## QuickBooks logos

All the approved Intuit branding and marketing assets that you may use in your product or when marketing your app can be obtained from the [QuickBooks Logo page](https://digitalasset.intuit.com/render/content/dam/intuit/sa/en_us/quickbooks/brand-design-guidelines/quickbooks-logo-50-50-external-for-editorial-brand.pdf).

If your application is spaced constrained and you must use an icon, [Download approved QuickBooks Logo Icon](/app/developer/logged-in-content/qb_logo_icon.zip).

### QuickBooks logo usage guidance

**Clear space and minimum size**
- Think of clear space as an invisible space around the logo artwork that protects its legibility and integrity.
- No visual elements should be placed inside of it.
- The margin should be half of the height of the QuickBooks symbol. This rule applies to any logo variation.

The minimum size protects the clear legibility of our logotype. The QuickBooks symbol in any logo variation can never be displayed under 16 pixels for digital (at 72dpi).

**What not to do**

Don't alter the QuickBooks logo in any way.

Below are some examples of what not to do with the QuickBooks logo in order to protect its integrity.

[Image: Logos-incorrect-ex-1.png]

[Image: Logos-incorrect-ex-2.png]

## Advertising restrictions

If you make references to QuickBooks or any other Intuit products or brand names in the advertising or promotion of your app (which includes advertising displays, marketing copy, web or print-based materials, and search engine marketing and ads) you must comply with the following advertising restrictions, consistent with our [Intuit Developer Terms](https://developer.intuit.com/app/developer/qbo/docs/legal-agreements/intuit-terms-of-service-for-intuit-developer-services). We will remove ads that do not comply.

### Pay-per-click and Search Engine Advertising

All sponsored ad titles must lead with your own marks or names, or with industry descriptors, and cannot lead with Intuit brands. For example, all sponsored ad titles must be structured as "XYZ for QuickBooks" instead of "QuickBooks XYZ."

Display URLs in search engine and other advertising cannot use or incorporate an Intuit Mark in or into the front portions of the URL, or into the root domain itself.

You may not bid on Intuit Marks (like "QuickBooks" and others described in the Developer Terms) as standalone keywords in search engines. You can only bid on keywords that include Intuit Marks as part of a larger phrase or search string to directly advertise apps that interoperate with Intuit products. For example, you may bid on keyword phrases that contain *both* QuickBooks and at least one additional word, like "CRM," "Sales Tax," "Point of Sale," "Inventory" and the like.

You are required to negative match for the specific search engine keywords below:

- Intuit
- QuickBooks
- Quick Books
- QB
- QBO
- QBSE
- QuickBooks Online
- QuickBooks Self-Employed
- QuickBooks Pro
- QuickBooks Premier
- QuickBooks Enterprise
- Intuit QuickBooks
- Intuit merchant
- Intuit QuickBooks online
- Intuit payroll
- QuickBooks payroll
- Intuit payments
- QuickBooks payments
- Www intuit com
- Intuit com
- QuickBooks tech support
- QuickBooks technical support
- QuickBooks phone support
- QuickBooks phone number
- QBO Intuit com
- QuickBooks intuit com
- Intuit com Intuit
- QuickBooks by Intuit
- ProAdvisor
- Intuit ProAdvisor
- QB ProAdvisor
- QuickBooks ProAdvisor
- Apps.com
- QuickBooks Support
- Mint
- Mint Bills
- TurboTax
- ProConnect
- ProSeries
- Intuit TurboTax
- Intuit Turbo
- Intuit Mint
- Turbo Mint
- Turbo

**Additional requirements:**

- If you advertise an app on search engines outside the US, you must ensure that it truly interoperates with the corresponding localized version of the Intuit product. Developers must designate the appropriate countries/regions for the ad.
- Intuit Marks may only be used in the very end segment of any display URL of a search engine ad (e.g., www.appdeveloper.com/appnameforquickbooks). Search engine ads must point to your own website, and a page containing actionable information about your app.
- When using Intuit Marks, avoid false claims or statements of affiliation, endorsement or sponsorship where no such relationship exists. For example, don't claim that the ad will lead people to an "Official Site" for QuickBooks, or claim that you are an "Official Partner" or "Preferred Solution" of Intuit, if that relationship does not exist.
- You can use words like "discount," "deal," or "low cost" in sponsored ads that also contain Intuit Marks, but you must avoid use of words that could negatively affect Intuit's brands, like "cheap," "blowout," "bargain," "fire sale," etc. We reserve the right to take down sponsored ads containing descriptions or words that we believe could damage the equity and reputation of our brands.

### Screenshot restrictions

You may use a limited number of screenshots from the Intuit software for illustrative purposes (e.g., educational guides, how-to books, training, product reviews, etc.), provided you comply with the following guidelines:

- You may not state or imply sponsorship, affiliation, authorization, recommendation, or endorsement by Intuit where no such relationship exists.
- You may not alter the screenshots in any way except to resize the screenshot in direct proportion to the original. Screenshots must be reproduced in their entirety. You may add commentary or other text only if clearly attributable to you and not Intuit.
- You may not use screenshots from Intuit beta products or other products that are subject to non-disclosure restrictions.
- You may not use screenshots that contain third party content unless you obtain the third party's permission.
- You may not use the screenshots in an ad comparing an Intuit offering to an Intuit competitor's offering.
- You may not use screenshots that contain images of identifiable individuals.
- You must include the following copyright attribution statement on all materials containing Intuit screenshots: "Screenshots © Intuit Inc. Used with permission."
- If your materials include references to an Intuit product, the full name of the product with corresponding trademark symbol should be shown in plain text at the first and/or most prominent mention (i.e., QuickBooks®, QB®).
- Your use of the screenshots may not be incorporated into obscene or pornographic material, and may not be disparaging, defamatory, or libelous to Intuit, any of its products, or any other person or entity (as determined by Intuit).
- Your materials should not be mostly or solely composed of Intuit screenshots or other Intuit intellectual property.
