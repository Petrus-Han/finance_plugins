# Entitlements

The Entitlements resource retrieves the features available to a company, identified by the company's realmID. The features available are determined by the type of company established during QuickBooks Online setup. These features are a super set of those enabled for the company by preferences and those enabled for a user by permissions.

> **Note**: This resource does not accept an application/json header. Use application/xml as the accept header.

## The Entitlements Object

### Attributes

| Attribute | Type | Description |
|-----------|------|-------------|
| **PlanName** | String | Billing plan associated with this company. |
| **Entitlement** | Array | Entitlement.id--Integer. Name of the entitlement. Entitlement.name--String. Name of the entitlement. Entitlement.Term--Boolean. Availability of entitlement: On or Off. |
| **SupportedLanguages** | String | Comma separated list of languages. |
| **TelephoneNumber** | String | Primary phone number. Max 20 chars. |
| **CompanyStartDate** | DateTime | DateTime when company file was created. This field and Metadata.CreateTime contain the same value. |
| **EmployerId** | String | Employer identifier (EIN). |
| **QboCompany** | Boolean | Check if the company is a QuickBooks Online company. false is returned if not a QuickBooks Online company, the company exists in the Intuit ecosystem, but is not a QuickBooks Online company, or the company is a QuickBooks Online company, but the current user does not belong to the company. |
| **Email** | EmailAddress | Default email address. Max 100 chars. |
| **WebAddr** | WebSiteAddress | Website address. |
| **FiscalYearStartMonth** | MonthEnum | The start month of fiscal year. |
| **Thresholds** | Array (minorVersion: 43) | The threshold for this company. |
| **DaysRemainingTrial** | Integer | Remaining trial period days. |
| **MaxUsers** | Integer | Maximum billable users allowed in the company. |
| **CurrentUsers** | Integer | Billable users currently in the company. |

### Sample Object

```xml
<EntitlementsResponse>
<QboCompany>true</QboCompany>
<PlanName>QBWEBPLUSPAYROLLMONTHLY</PlanName>
<MaxUsers>10</MaxUsers>
<CurrentUsers>4</CurrentUsers>
<DaysRemainingTrial>0</DaysRemainingTrial>
<Entitlement id="7">
<name>PayPal</name>
<term>Off</term>
</Entitlement>
<Entitlement id="8">
<name>Merchant Service</name>
<term>Off</term>
</Entitlement>
<Entitlement id="1">
<name>Class Tracking</name>
<term>On</term>
</Entitlement>
<Entitlement id="3">
<name>Expense Tracking by Customer</name>
<term>On</term>
</Entitlement>
<Entitlement id="4">
<name>Time Tracking</name>
<term>On</term>
</Entitlement>
<Entitlement id="5">
<name>Budgets</name>
<term>On</term>
</Entitlement>
<Entitlement id="6">
<name>Custom Invoice Styles</name>
<term>On</term>
</Entitlement>
<Entitlement id="9">
<name>1099 Forms for Vendors</name>
<term>On</term>
</Entitlement>
<Entitlement id="10">
<name>Managing Bills to Pay Later</name>
<term>On</term>
</Entitlement>
<Entitlement id="11">
<name>Complete Set of Reports</name>
<term>On</term>
</Entitlement>
<Entitlement id="12">
<name>Enhanced Reporting</name>
<term>On</term>
</Entitlement>
<Entitlement id="13">
<name>Exporting to Excel</name>
<term>On</term>
</Entitlement>
<Entitlement id="15">
<name>Delayed Charges</name>
<term>On</term>
</Entitlement>
<Entitlement id="16">
<name>Custom Sales Fields</name>
<term>On</term>
</Entitlement>
<Entitlement id="17">
<name>More Users -- up to 20</name>
<term>On</term>
</Entitlement>
<Entitlement id="19">
<name>Recurring Transactions</name>
<term>On</term>
</Entitlement>
<Entitlement id="20">
<name>Closing the Books</name>
<term>On</term>
</Entitlement>
<Entitlement id="21">
<name>Location Tracking</name>
<term>On</term>
</Entitlement>
<Entitlement id="22">
<name>More Names</name>
<term>On</term>
</Entitlement>
<Entitlement id="25">
<name>Custom Home Page</name>
<term>On</term>
</Entitlement>
<Entitlement id="26">
<name>Do-it-yourself Payroll</name>
<term>On</term>
</Entitlement>
<Entitlement id="28">
<name>Online Banking</name>
<term>On</term>
</Entitlement>
<Entitlement id="29">
<name>Basic Sales</name>
<term>On</term>
</Entitlement>
<Entitlement id="30">
<name>Basic Banking</name>
<term>On</term>
</Entitlement>
<Entitlement id="31">
<name>Accounting</name>
<term>On</term>
</Entitlement>
<Entitlement id="33">
<name>Reports Only User</name>
<term>On</term>
</Entitlement>
<Entitlement id="35">
<name>Estimates</name>
<term>On</term>
</Entitlement>
<Entitlement id="41">
<name>Company Snapshot</name>
<term>On</term>
</Entitlement>
<Entitlement id="42">
<name>Purchase Order</name>
<term>On</term>
</Entitlement>
<Entitlement id="43">
<name>Inventory</name>
<term>On</term>
</Entitlement>
<Entitlement id="44">
<name>Do-it-yourself Payroll (Paycycle)</name>
<term>Off</term>
</Entitlement>
<Entitlement id="45">
<name>Multi-Currency</name>
<term>On</term>
</Entitlement>
<Entitlement id="46">
<name>Trends</name>
<term>On</term>
</Entitlement>
<Entitlement id="47">
<name>Hide Employee List</name>
<term>Off</term>
</Entitlement>
<Entitlement id="48">
<name>Simple Report List</name>
<term>Off</term>
</Entitlement>
<Entitlement id="49">
<name>Global Tax Model</name>
<term>On</term>
</Entitlement>
<Entitlement id="52">
<name>Accountant Menu</name>
<term>On</term>
</Entitlement>
<Thresholds>
<threshold>
<name>CLASSES_AND_DEPARTMENTS</name>
<limit>40</limit>
<enforced>true</enforced>
<currentCount>19</currentCount>
<aboveThreshold>false</aboveThreshold>
</threshold>
<threshold>
<name>ACCOUNTS</name>
<limit>250</limit>
<enforced>true</enforced>
<currentCount>7</currentCount>
<aboveThreshold>false</aboveThreshold>
</threshold>
<threshold>
<name>USERS</name>
<limit>5</limit>
<enforced>true</enforced>
<currentCount>1</currentCount>
<aboveThreshold>false</aboveThreshold>
</threshold>
<threshold>
<name>ACCOUTANTS</name>
<limit>2</limit>
<enforced>false</enforced>
<currentCount>-2</currentCount>
<aboveThreshold>false</aboveThreshold>
</threshold>
<threshold>
<name>CUSTOMFIELD_ALL</name>
<limit>6</limit>
<enforced>false</enforced>
<currentCount>0</currentCount>
<aboveThreshold>false</aboveThreshold>
</threshold>
<threshold>
<name>CUSTOMFIELD_PO</name>
<limit>3</limit>
<enforced>false</enforced>
<currentCount>0</currentCount>
<aboveThreshold>false</aboveThreshold>
</threshold>
<threshold>
<name>CUSTOMFIELD_SALES</name>
<limit>3</limit>
<enforced>false</enforced>
<currentCount>0</currentCount>
<aboveThreshold>false</aboveThreshold>
</threshold>
</Thresholds>
</EntitlementsResponse>
```

## Read Entitlements

Retrieves the entitlements details.

### Request URL

```
GET /entitlements/v3/<realmID>
Production Base URL (OAUTH1): https://qbo.sbfinance.intuit.com/manage
Production Base URL (OAUTH2): https://quickbooks.api.intuit.com/manage
Sandbox Base URL (OAUTH1): https://qbo.sbfinance.intuit.com/manage
Sandbox Base URL (OAUTH2): https://sandbox-quickbooks.api.intuit.com/manage
```

### Response

```xml
<EntitlementsResponse>
<QboCompany>true</QboCompany>
<PlanName>QBWEBPLUSPAYROLLMONTHLY</PlanName>
<MaxUsers>10</MaxUsers>
<CurrentUsers>4</CurrentUsers>
<DaysRemainingTrial>0</DaysRemainingTrial>
<Entitlement id="7">
<name>PayPal</name>
<term>Off</term>
</Entitlement>
<Entitlement id="8">
<name>Merchant Service</name>
<term>Off</term>
</Entitlement>
<Entitlement id="1">
<name>Class Tracking</name>
<term>On</term>
</Entitlement>
<Entitlement id="3">
<name>Expense Tracking by Customer</name>
<term>On</term>
</Entitlement>
<Entitlement id="4">
<name>Time Tracking</name>
<term>On</term>
</Entitlement>
<Entitlement id="5">
<name>Budgets</name>
<term>On</term>
</Entitlement>
<Entitlement id="6">
<name>Custom Invoice Styles</name>
<term>On</term>
</Entitlement>
<Entitlement id="9">
<name>1099 Forms for Vendors</name>
<term>On</term>
</Entitlement>
<Entitlement id="10">
<name>Managing Bills to Pay Later</name>
<term>On</term>
</Entitlement>
<Entitlement id="11">
<name>Complete Set of Reports</name>
<term>On</term>
</Entitlement>
<Entitlement id="12">
<name>Enhanced Reporting</name>
<term>On</term>
</Entitlement>
<Entitlement id="13">
<name>Exporting to Excel</name>
<term>On</term>
</Entitlement>
<Entitlement id="15">
<name>Delayed Charges</name>
<term>On</term>
</Entitlement>
<Entitlement id="16">
<name>Custom Sales Fields</name>
<term>On</term>
</Entitlement>
<Entitlement id="17">
<name>More Users -- up to 20</name>
<term>On</term>
</Entitlement>
<Entitlement id="19">
<name>Recurring Transactions</name>
<term>On</term>
</Entitlement>
<Entitlement id="20">
<name>Closing the Books</name>
<term>On</term>
</Entitlement>
<Entitlement id="21">
<name>Location Tracking</name>
<term>On</term>
</Entitlement>
<Entitlement id="22">
<name>More Names</name>
<term>On</term>
</Entitlement>
<Entitlement id="25">
<name>Custom Home Page</name>
<term>On</term>
</Entitlement>
<Entitlement id="26">
<name>Do-it-yourself Payroll</name>
<term>On</term>
</Entitlement>
<Entitlement id="28">
<name>Online Banking</name>
<term>On</term>
</Entitlement>
<Entitlement id="29">
<name>Basic Sales</name>
<term>On</term>
</Entitlement>
<Entitlement id="30">
<name>Basic Banking</name>
<term>On</term>
</Entitlement>
<Entitlement id="31">
<name>Accounting</name>
<term>On</term>
</Entitlement>
<Entitlement id="33">
<name>Reports Only User</name>
<term>On</term>
</Entitlement>
<Entitlement id="35">
<name>Estimates</name>
<term>On</term>
</Entitlement>
<Entitlement id="41">
<name>Company Snapshot</name>
<term>On</term>
</Entitlement>
<Entitlement id="42">
<name>Purchase Order</name>
<term>On</term>
</Entitlement>
<Entitlement id="43">
<name>Inventory</name>
<term>On</term>
</Entitlement>
<Entitlement id="44">
<name>Do-it-yourself Payroll (Paycycle)</name>
<term>Off</term>
</Entitlement>
<Entitlement id="45">
<name>Multi-Currency</name>
<term>On</term>
</Entitlement>
<Entitlement id="46">
<name>Trends</name>
<term>On</term>
</Entitlement>
<Entitlement id="47">
<name>Hide Employee List</name>
<term>Off</term>
</Entitlement>
<Entitlement id="48">
<name>Simple Report List</name>
<term>Off</term>
</Entitlement>
<Entitlement id="49">
<name>Global Tax Model</name>
<term>On</term>
</Entitlement>
<Entitlement id="52">
<name>Accountant Menu</name>
<term>On</term>
</Entitlement>
<Thresholds>
<threshold>
<name>CLASSES_AND_DEPARTMENTS</name>
<limit>40</limit>
<enforced>true</enforced>
<currentCount>19</currentCount>
<aboveThreshold>false</aboveThreshold>
</threshold>
<threshold>
<name>ACCOUNTS</name>
<limit>250</limit>
<enforced>true</enforced>
<currentCount>7</currentCount>
<aboveThreshold>false</aboveThreshold>
</threshold>
<threshold>
<name>USERS</name>
<limit>5</limit>
<enforced>true</enforced>
<currentCount>1</currentCount>
<aboveThreshold>false</aboveThreshold>
</threshold>
<threshold>
<name>ACCOUTANTS</name>
<limit>2</limit>
<enforced>false</enforced>
<currentCount>-2</currentCount>
<aboveThreshold>false</aboveThreshold>
</threshold>
<threshold>
<name>CUSTOMFIELD_ALL</name>
<limit>6</limit>
<enforced>false</enforced>
<currentCount>0</currentCount>
<aboveThreshold>false</aboveThreshold>
</threshold>
<threshold>
<name>CUSTOMFIELD_PO</name>
<limit>3</limit>
<enforced>false</enforced>
<currentCount>0</currentCount>
<aboveThreshold>false</aboveThreshold>
</threshold>
<threshold>
<name>CUSTOMFIELD_SALES</name>
<limit>3</limit>
<enforced>false</enforced>
<currentCount>0</currentCount>
<aboveThreshold>false</aboveThreshold>
</threshold>
</Thresholds>
</EntitlementsResponse>
```
