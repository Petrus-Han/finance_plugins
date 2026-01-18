# Common reasons why apps do not pass review

If you're [listing your app on the QuickBooks App Store](/app/developer/qbo/docs/go-live/list-on-the-app-store), it needs to go through a [review process](/app/developer/qbo/docs/go-live/list-on-the-app-store/what-to-expect-during-the-review).

During the review, we'll assess the quality and functionality of your app. We'll also check if it meets our branding requirements. Not all apps pass this review.

Here are common reasons why apps may fail parts, or all, of the review.

## The Get App Now link on your app's QuickBooks App Store page doesn't go to SSO page

Review the [technical requirements](/app/developer/qbo/docs/go-live/publish-app/technical-requirements) before submitting your app for review. Make sure you know [how Intuit Single Sign-on works](/app/developer/qbo/docs/develop/authentication-and-authorization/single-sign-on-models).

## Users can't request a trial or demo

Users need to be able to request a trial or demo.

For apps that don't use Intuit Single Sign-on, your app's "Learn More" page needs to explain how the app specifically integrates with QuickBooks.

## Users can't find QuickBooks integration settings within your app

It may not be clear to users that your app integrates with QuickBooks. Users may also have to change their settings to fully integrate your app with QuickBooks. This is a common reason for rejection.

If users need to change settings within your app to make it work with QuickBooks, make this very clear.

## Data flow between your app and QuickBooks doesn't work as expected

Review the "QuickBooks Data Connection" section of our [Technical requirements](/app/developer/qbo/docs/go-live/publish-app/technical-requirements) to learn more.

## Sign in UI and button is missing or outdated

Review the "Sign in with Intuit Button" section of our [Technical requirements](/app/developer/qbo/docs/go-live/publish-app/technical-requirements) to learn more.

Here are a few reasons we may flag an app:

- App doesn't use the required "Connect to QuickBooks" button
- App doesn't use the required "Sign in with Intuit" button
- App uses outdated QuickBooks logo
