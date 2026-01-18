# Build a Demo App

> **Source**: https://developer.intuit.com/app/developer/qbo/docs/get-started/build-your-first-app

## Quick Start Options

If you just want to jump right in and test an API call, you have a few options:

### Make a Generic API Call

Simply [set up your developer account](https://developer.intuit.com/app/developer/qbo/docs/get-started/start-developing-your-app). Then use the sample GET request to call the **companyInfo** entity.

### Call a Specific API Using Your Sandbox Company

1. [Sign in](https://developer.intuit.com/dashboard) to your developer account.
2. [Visit the API Explorer](https://developer.intuit.com/app/developer/qbo/docs/api/accounting/most-commonly-used/account).
3. Choose a sandbox company from the dropdown.
4. Find an API entity and operation.
5. Select **Try it**.

---

## Build a Demo App

Want to build something more robust that mimics the early stages of app development? Use this guide to build a "Demo app" in .NET, Java, or PHP. The demo can send requests and get live data from QuickBooks Online.

---

## .NET Guide

### Step 1: Clone the "Hello World" Repository

Before you start, you should have a basic understanding of **ASP.NET MVC Framework**.

**Prerequisites:**
- Visual Studio 2015 or later
- .Net framework 4.6.1
- IIS or IIS Express 8.0

**Clone the repository:**

```bash
git clone https://github.com/IntuitDeveloper/HelloWorldApp-MVC5-Dotnet
cd HelloWorldApp-MVC5-Dotnet
```

This repo gives you basic code to build the demo app. It sets up your development environment so you can [use an SDK](https://developer.intuit.com/app/developer/qbo/docs/develop/sdks-and-samples), handles authorization [set up (OAuth 2.0 protocol)](https://developer.intuit.com/app/developer/qbo/docs/develop/authentication-and-authorization/oauth-2.0), and simplifies logging.

### Step 2: Create a Demo App on the Intuit Developer Portal

1. [Sign in](https://developer.intuit.com/dashboard) to your developer account.
2. Select **My Hub > App dashboard** from the upper-right corner of the toolbar. You will be redirected to your default workspace.
3. To open another workspace, select it from the dropdown next to **Workspaces >**.
4. Create an app specifically for this demo, named "Demo app".
5. Select the **Accounting** scope on the **Add permissions** page and then select **Done**.

This generates credentials and lets you set the demo's URIs. You can use these credentials on a QuickBooks Online Sandbox company. [Click here](https://developer.intuit.com/sandbox-companies) to create one.

### Step 3: Get the Demo App's Credentials

1. [Sign in](https://developer.intuit.com/dashboard) to your developer account.
2. Select **My Hub > App dashboard** from the upper-right corner of the toolbar.
3. Select and open the **Demo app** app you just created.
4. Select **Keys and credentials** from the left navigation pane.
5. Choose **Development** and turn on the **Show credentials** switch.
6. Copy the **Client ID** and **Client secret**.

### Step 4: Add the Cloned "Hello World" Repo's Redirect URI

When users connect to your app, it needs to redirect them to start the authorization flow. This "user consent" step is where they give your app permission to access their QuickBooks Online company data.

Let's redirect users who connect to your "Demo app" to the callback page:

1. [Sign in](https://developer.intuit.com/dashboard) to your developer account.
2. Select **My Hub > App dashboard** from the upper-right corner of the toolbar.
3. Select and open **Demo app**.
4. Select **Settings** from the left navigation pane.
5. Select the **Redirect URIs** tab, then select **Development**.
6. Enter: `http://localhost:27353/callback`.
7. Select **Save**.

### Step 5: Configure the Authorization Flow

For this demo app, we'll assume a user [found your app on the QuickBooks App Store](https://developer.intuit.com/app/developer/qbo/docs/go-live/list-on-the-app-store) and selected the **Connect to QuickBooks** link.

**Edit the Web.config file:**

1. Open and [edit the Web.config file](https://github.com/IntuitDeveloper/HelloWorldApp-MVC5-Dotnet/blob/master/MvcCodeFlowClientManual/Web.config) in the root directory of the "Hello World" repo you cloned in Step 1.
2. Edit the file using the sample code below.
3. Enter the **Client ID** and **Client secret** for your demo app.
4. Review the **Redirect URI**.

```xml
<appSettings>
    <add key="clientid" value="Enter value here" />
    <add key="clientsecret" value="Enter value here" />
    <add key="redirectUrl" value="http://localhost:27353/callback" />
</appSettings>
```

### Step 6: Simulate the Authorization Flow

1. Launch your app in **Visual Studio**.
2. Select **Connect to QuickBooks**.
3. Follow the onscreen steps to connect a sandbox company. Sign in using the same sign-in and password as your developer account.
4. Select **Authorize**.

After you select Authorize, you'll redirect to the URI you added in Step 4.

### Step 7: Make Your First API Call

If users authorize your app, our server sends an authorization code to your app. You'll exchange the authorization code for access tokens. For this demo, the Intuit OAuth 2.0 server will automatically handle the backend exchange of temporary authorization codes for tokens.

Let's assume the "Demo app" has access tokens and simulate your first API call. You'll redirect to a new webpage via the URI (i.e., `http://localhost:27353/callback`).

This automatically makes an API call to the `CompanyInfo` entity for the sandbox company you just connected.

### Start Building Your App Using a .NET SDK

Now you have a good understanding of the basic development and authorization process. [Download one of our SDKs](https://developer.intuit.com/app/developer/qbo/docs/develop/sdks-and-samples) to get a jumpstart on development.

---

## Code Reference (.NET)

### Web.config

The **Client Id** and **Client Secret** are used by your app to uniquely establish its identity with the QuickBook Online platform.

The value of **Redirect URI** defines where your app's users get redirected in your app after they authorize the app.

Specify which environment your application is running in with **appEnvironment** value. This ensures the **OAuth2Client** uses the [correct discovery document](https://developer.intuit.com/app/developer/qbo/docs/develop/authentication-and-authorization/oauth-openid-discovery-doc) (this is part of the **OAuth2Client** initialization). Discovery documents contain the **AuthorizationEndpoint**, **TokenEndpoint**, and other values required for the authorization flow.

```xml
<appSettings>
    <add key="clientid" value="EnterClientIdHere" />
    <add key="clientsecret" value="EnterClientSecretHere" />
    <add key="appEnvironment" value="sandbox" />
    <add key="redirectUrl" value="http://localhost:27353/callback" />
</appSettings>
```

### AppController

#### Initialize OAuth2Client Object

```csharp
public static OAuth2Client auth2Client = new OAuth2Client(clientid, clientsecret, redirectUrl, environment);
```

#### InitiateAuth (string submitButton)

To start the authorization flow, specify the **Accounting** scope. Use **GetAuthorizationURL** method of **OAuth2Client** object to get the Authorization URL:

```csharp
public ActionResult InitiateAuth(string submitButton)
{
    List<OidcScopes> scopes = new List<OidcScopes>();
    scopes.Add(OidcScopes.Accounting);
    string authorizeUrl = auth2Client.GetAuthorizationURL(scopes);
    return Redirect(authorizeUrl);
}
```

#### ApiCallService()

Once the tokens are received, apps can make calls to the QuickBooks Online Accounting API:

1. First, create a **ServiceContext** object. **ServiceContext** is created with API **Access Token** along with the **realmId** and works as a context for the API request.
2. This **ServiceContext** object can then be used in **QueryService** to query for **CompanyInfo** data.
3. **QueryService** can be used to execute any API [supported query](https://developer.intuit.com/app/developer/qbo/docs/learn/explore-the-quickbooks-online-api/data-queries) as a string in a parameter.

```csharp
public ActionResult ApiCallService()
{
    string realmId = Session["realmId"].ToString();
    var principal = User as ClaimsPrincipal;
    OAuth2RequestValidator oauthValidator = new OAuth2RequestValidator(principal.FindFirst("access_token").Value);
    
    // Create a ServiceContext with Auth tokens and realmId
    ServiceContext serviceContext = new ServiceContext(realmId, IntuitServicesType.QBO, oauthValidator);
    serviceContext.IppConfiguration.MinorVersion.Qbo = "23";

    // Create a QuickBooks QueryService using ServiceContext
    QueryService<CompanyInfo> querySvc = new QueryService<CompanyInfo>(serviceContext);
    CompanyInfo companyInfo = querySvc.ExecuteIdsQuery("SELECT * FROM CompanyInfo").FirstOrDefault();

    string output = JsonConvert.SerializeObject(companyInfo, new JsonSerializerSettings
    {
        NullValueHandling = NullValueHandling.Ignore
    });
    return View("ApiCallService", (object)("QBO API call Successful!! Response: " + output));
}
```

### CallbackController

#### Index()

After user clicks on **Connect** button in authorization flow, the request is sent to Intuit servers. When successful, Intuit responds with an authorization code and the QuickBooks Company ID (i.e., the **Realm ID**) on the **Redirect URL** as callback URL query parameters.

```csharp
public async Task<ActionResult> Index()
{
    string code = Request.QueryString["code"] ?? "none";
    string realmId = Request.QueryString["realmId"] ?? "none";
    await GetAuthTokensAsync(code, realmId);
}
```

#### GetAuthTokensAsync(string code, string realmId)

This authorization code is exchanged for **Access and Refresh Tokens** using the **TokenEndpoint**. **Access tokens** are used in an API request and **Refresh tokens** are used to get fresh short-lived **Access tokens** after they expire.

```csharp
private async Task GetAuthTokensAsync(string code, string realmId)
{
    var tokenResponse = await auth2Client.GetBearerTokenAsync(code);
    var accessToken = tokenResponse.AccessToken;
    var refreshToken = tokenResponse.RefreshToken;
}
```

---

## Java Guide

The Java guide follows the same 7-step process:

1. Clone the "Hello world" repository
2. Create a demo app on the Intuit Developer Portal
3. Get the demo app's credentials
4. Add the cloned "Hello world" repo's redirect URI
5. Configure the authorization flow
6. Simulate the authorization flow
7. Make your first API call

**Repository**: https://github.com/IntuitDeveloper/HelloWorld-Java

---

## PHP Guide

The PHP guide follows the same 7-step process:

1. Clone the "Hello world" repository
2. Create a demo app on the Intuit Developer Portal
3. Get the demo app's credentials
4. Add the cloned "Hello world" repo's redirect URI
5. Configure the authorization flow
6. Simulate the authorization flow
7. Make your first API call

**Repository**: https://github.com/IntuitDeveloper/HelloWorld-PHP

---

## Mercury Integration Notes

For the Mercury-QuickBooks sync plugin:

1. **OAuth Flow**: The demo app pattern shows how to implement OAuth 2.0 authorization. The plugin will need similar credential management.

2. **ServiceContext Pattern**: The .NET example shows how to create a ServiceContext with access tokens and realm ID - this pattern applies to all API calls.

3. **Query Pattern**: The `QueryService.ExecuteIdsQuery()` pattern can be used to query existing data before creating new records (e.g., checking for existing vendors).

4. **Sandbox Testing**: Use sandbox companies for development and testing before connecting to production QuickBooks companies.
