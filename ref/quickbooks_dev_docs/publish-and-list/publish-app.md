# Publish Your App

Publish your app and put it into production. This makes it live and functional. You can share the URL of the app with users so they can access it.

Follow these steps to get production credentials. Use them in your code to make your app live and ready to use.

If you want to make your app publicly available, here's how to [list your app on the QuickBooks App Store](list-on-the-app-store.md).

---

## Step 1: Fill out the App Details for Production

1. [Sign in](https://developer.intuit.com/dashboard) to your developer account.
2. Select **My Hub > App dashboard** from the upper-right corner of the toolbar.
3. Select and open the app you want to publish.
4. Select **Keys and credentials** from the left navigation pane.
5. Select **Production**.
6. Select **App Details** and fill in all the details.
7. Select the down arrow of the first section and fill in your email address and other details.
8. In the next section, enter the URLs for your End User License Agreement and Privacy Policy.
9. In the next, add your app's host domain, launch URL, and redirect URL.
10. In the next, select up to four categories for your app. These help your users understand what your app does.
11. In the next, check any regulated industries that you built the app for.
12. Select the regions where your app is hosted.

This should take about 30 minutes to complete.

---

## Step 2: Review OAuth 2.0

Make sure you've fully [set up OAuth 2.0](../develop/authentication-and-authorization/oauth-2.0.md) for your app.

Before you go live, try connecting, disconnecting and reconnecting your app from a sandbox company. This helps catch and prevent errors in your OAuth2.0 setup.

---

## Step 3: Update your Intuit Developer Account profile

1. [Sign in](https://developer.intuit.com/dashboard) to your developer account.
2. Select **My Hub > Account Profile** from the upper-right corner of the toolbar.
3. Review your contact and account info.

---

## Step 4: Complete the App Assessment Questionnaire

1. [Sign in](https://developer.intuit.com/dashboard) to your developer account.
2. Select **My Hub > Account Profile** from the upper-right corner of the toolbar.
3. Select and open the app you want to publish.
4. Go to **Keys and credentials** from the left navigation pane.
5. Select **Production** and then select **Compliance**.
6. Select **Start Questionnaire**.
7. Complete the questionnaire.

These URLs are required before you can get your production credentials.

---

## Step 5: Review your app's name, icon, and other settings

With the app still open on your developer account:

1. Review the [naming and logo guidelines](list-on-the-app-store/naming-and-logo-guidelines.md) for published apps.
2. [Sign in](https://developer.intuit.com/dashboard) to your developer account.
3. Select and open the app you want to publish.
4. Select **Settings** from the left navigation pane.
5. Select the **Basic app info** tab and review the app name and the icon. Upload the image you want users to see when they download your app.
6. Check the rest of the tabs to ensure that all information is correct.

---

## Step 6: Get your app's production credentials

Now you have all the correct info and settings in place. It's time to get your app's Client ID and Client Secret so you can code it into your app and make calls to our API.

1. [Sign in](https://developer.intuit.com/dashboard) to your developer account.
2. Select and open the app you want to publish.
3. Select **Keys and credentials** from the left navigation pane.
4. Select **Production** and turn on **Show Credentials**. Note: The **Show Credentials** switch appears only after the App Assessment Questionnaire is approved.
5. Copy the **Client ID** and **Client secret**.

Use these credentials for your production app. Put them into relevant variables and settings in your code. This gives your app access QuickBooks Online data and our API.

You can share the URL with other developers or users so they can access your app, keeping it semi-private.

---

## Next steps: List on the QuickBooks App Store

If you want to use your app privately, it's now live and functional.

Want to make your app publicly available to millions of QuickBooks Online users? Here's how to [list your app on the QuickBooks App Store](list-on-the-app-store.md).

---

## Related Pages

- [Publishing requirements and guidelines](publish-app/platform-requirements.md)
- [Technical requirements](publish-app/technical-requirements.md)
- [Security requirements](publish-app/security-requirements.md)
- [Marketing requirements](publish-app/marketing-requirements.md)

---

*Source: https://developer.intuit.com/app/developer/qbo/docs/go-live/publish-app*
