# Password policy for Intuit Developer Services

## PURPOSE
The purpose of this policy is to ensure the creation of strong passwords, the protection of those passwords, and the frequency of change for passwords for applications that integrate with Intuit Services. This policy sets forth minimum requirements. You are encouraged to implement a stronger password policy.

## SCOPE
This policy applies to the Intuit Developer Group’s customer facing platforms.

## DEFINITIONS
- **Effective Passwords**: Passwords should be difficult to guess, yet easy to remember.
- **Financial Data API**: Provides developers access to end-user financial account and transactional information from financial institutions.
- **QuickBooks Accounting API**: A set of coding components and web services you can use to leverage and extend QuickBooks Online features.
- **QuickBooks Desktop QBXML SDK**: Allows you to develop desktop software solutions that integrate with QuickBooks for Windows.
- **Payments API**: A service that processes credit card payments.

## Credential Creation Requirements for Financial Data and Payments APIs
A password system shall enforce a minimum length of six characters. The password system must support passwords up to at least 128 characters.
A password shall consist of the following:
- Letters [required 1]: a-z, A-Z – AND
- Numbers [optional 1]: 0-9 – OR
- Symbols [optional 1]: ~, !, @, #, $, %, ^, &, *, (, ), -, _, =, +, [, {, ], }, \, |, ;, :, ‘, “, ,, ., <, >, /, ?
- Verify password is not contained in standard dictionaries.
- Verify password is not the same as, or a trivial variation of the username.
- Password system must support mixed case passwords.
- Passwords will expire no later than 120 consecutive days after issuance.
- Products must accommodate Account ID lockout after 10 consecutive failed login attempts (locked for min 24 hours).
- After expiration, user must select a new password (cannot be one of previous 5).
- User may not change password more than 1 time per hour.

## Credential Creation Requirements for QuickBooks Accounting Services
A password system shall enforce a minimum length of six characters. The password system must support passwords up to at least 128 characters.
A password shall consist of the following:
- Letters [required]: a-z, A-Z
- Numbers [optional]: 0-9
- Symbols [optional]: standard symbols list.

## Credential Reset
- Alternate "something the user knows" challenge should be presented (e.g., challenge questions).
- Email is not considered an authentication factor but can add a protective step.

## Credential Transmission
(For Financial Data or Payments APIs)
- Account IDs and Passwords must be protected with encryption during transmission.
- SSL Server certificate must maintain grade A or B (SSL Labs).
- Disable password auto-complete.

## Credential Storage
(For Financial Data or Payments APIs)
- Account IDs may be stored in plain text.
- Passwords must NOT be stored in plain text.
- Passwords must be one-way hashed (bcrypt, scrypt, or PBKDF2) with unique salt.
- Application must not store End-user credentials for another source (e.g., bank) unless approved. If approved, Account ID must be encrypted (AES-256).
