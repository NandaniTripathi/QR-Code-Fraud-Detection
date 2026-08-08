# QR Shield

## AI-Powered QR Code Threat Intelligence Platform

[![Python](https://img.shields.io/badge/Python-3.x-blue?logo=python)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Backend-Flask-black?logo=flask)](https://flask.palletsprojects.com/)
[![Streamlit](https://img.shields.io/badge/Frontend-Streamlit-red?logo=streamlit)](https://streamlit.io/)
[![SQLite](https://img.shields.io/badge/Database-SQLite-blue?logo=sqlite)](https://www.sqlite.org/)
[![GitHub](https://img.shields.io/badge/Repository-GitHub-black?logo=github)](https://github.com/NandaniTripathi/QR-Code-Fraud-Detection)

**Repository:**  
https://github.com/NandaniTripathi/QR-Code-Fraud-Detection

---

## Overview

QR Shield is a security-focused web application designed to analyze QR codes and identify potentially suspicious or risky payloads before users interact with them.

The platform combines QR code decoding, payload classification, phishing detection, URL security analysis, domain intelligence, IP intelligence, hosting information, and external threat-intelligence services into a unified security dashboard.

The project focuses on the security risks associated with malicious QR codes, including QR-based phishing and suspicious URL redirection.

---

## Problem Statement

QR codes have become widely used for websites, payments, authentication, contact sharing, WiFi configuration, and other digital interactions.

However, a QR code itself does not reveal where it will redirect a user.

Attackers can use QR codes to hide malicious URLs, phishing websites, suspicious redirects, or other potentially harmful content.

QR Shield addresses this problem by allowing users to:

1. Upload a QR code.
2. Decode its embedded payload.
3. Identify the payload type.
4. Analyze suspicious characteristics.
5. Gather additional threat intelligence.
6. Generate a risk score and risk level.
7. Present the results through a security dashboard.

---

# Key Features

## 1. QR Code Decoding

The application accepts QR code images and extracts their embedded data.

Supported payload categories include:

- URL
- WiFi
- vCard
- Email
- SMS
- Phone
- Location
- UPI Payment
- Plain Text

---

## 2. Payload Analysis

After decoding the QR code, the application identifies the type of payload and displays the extracted content.

For URL-based QR codes, additional security analysis is performed.

For non-URL QR codes, the application identifies the payload type without performing URL-specific threat analysis.

---

## 3. Phishing Detection

QR Shield evaluates URLs using security rules designed to identify suspicious characteristics.

The analysis includes indicators such as:

- Missing HTTPS
- IP-based URLs
- Long URLs
- Suspicious keywords
- Suspicious top-level domains
- URL shorteners
- Multiple suspicious URL characteristics

These indicators contribute to the overall risk assessment.

---

## 4. Risk Scoring

The application generates a numerical risk score based on detected security indicators.

The result is presented as:

```text
Risk Score
     |
     v
Security Rules
     |
     v
Threat Indicators
     |
     v
Risk Level
