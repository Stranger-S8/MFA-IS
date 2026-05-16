# MFA IS

A desktop multi-factor authentication demo using Firebase Firestore and email-based verification codes.

## Overview

MFA IS is a CustomTkinter authentication project that demonstrates registration, login, Firestore-backed user lookup, encrypted admin credentials, and email verification codes with an expiry window.

## Key Features

- Desktop login and registration UI
- Firebase Firestore user storage
- Email verification code flow
- Local encrypted credential helper
- Verification timeout handling

## Tech Stack

- Python
- CustomTkinter
- Firebase Admin SDK
- Firestore
- SMTP email
- Pillow

## Project Structure

```text
.
|-- main.py          # Desktop application
|-- encryption.py    # Credential storage helper
|-- key.json         # Local Firebase service account file
|-- credentials/     # Local credential material
|-- images/          # UI assets
`-- documentation/   # Project docs
```

## Getting Started

```bash
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python main.py
```

## Configuration

Add your Firebase service account as `key.json` for local use only. Configure SMTP credentials through the encrypted credential helper before sending email verification codes.

## GitHub Notes

Never commit `key.json`, real credentials, SMTP passwords, or private user data.
