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
<img width="1333" height="585" alt="WhatsApp Image 2026-08-08 at 10 43 22 AM" src="https://github.com/user-attachments/assets/4edf6dc0-b4b7-417e-a162-5a0b7f1f67bd" />


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

<img width="1366" height="598" alt="WhatsApp Image 2026-08-08 at 10 44 54 AM" src="https://github.com/user-attachments/assets/a282670f-c824-4ab3-8e06-05bb89b37c0d" />


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

<img width="1366" height="588" alt="WhatsApp Image 2026-08-08 at 10 46 08 AM" src="https://github.com/user-attachments/assets/cef10f6d-28b3-47de-ae41-36e2eaaa8a52" />


5. VirusTotal Integration
QR Shield can integrate VirusTotal threat intelligence to provide additional information about URLs or files.

The dashboard can display:

Malicious detections

Suspicious detections

Harmless detections

This provides an additional layer of external security intelligence.

6. WHOIS / Domain Intelligence
The application performs domain-related analysis and can retrieve information such as domain age.

Domain information can be used as an additional signal when evaluating suspicious URLs.

7. IP Intelligence
For applicable URLs, QR Shield can retrieve IP-related information including:

IP address

Country

City

ISP

Organization

ASN

This provides additional context about the infrastructure associated with a URL.

<img width="1366" height="589" alt="WhatsApp Image 2026-08-08 at 10 47 44 AM" src="https://github.com/user-attachments/assets/a0eb6f09-d403-445c-b225-3d0f185741c0" />


8. Hosting Provider Detection
The application attempts to identify the hosting provider associated with the analyzed URL or infrastructure.

The dashboard displays:

Hosting provider

Classification / risk information

<img width="1366" height="596" alt="WhatsApp Image 2026-08-08 at 10 48 34 AM" src="https://github.com/user-attachments/assets/5518fa62-3354-4ecf-a93d-bc30d6c33b6b" />


9. SSL Analysis
QR Shield includes an SSL analysis module for evaluating HTTPS and certificate-related information.

This provides an additional security signal when analyzing URLs.

10. Safe Browsing Checks
The project includes a Safe Browsing threat-intelligence module for additional URL security analysis.

11. Downloadable File Analysis
When applicable, QR Shield can analyze downloadable files associated with a URL.

The dashboard can display:

Malicious

Suspicious

Harmless

results from the available analysis service.

12. Scan History
QR Shield maintains a local scan history using SQLite.

The dashboard allows users to:

View previous scans

Search scan records

Review payload types

Review decoded URLs

Review risk scores

Review risk levels

Review scan timestamps

Export scan history as CSV

<img width="1366" height="596" alt="WhatsApp Image 2026-08-08 at 10 49 42 AM" src="https://github.com/user-attachments/assets/fa6a12ae-c2cd-49e6-bf96-075f401704c0" />


Disclaimer
QR Shield is an educational and portfolio project created for QR-code security analysis and threat-intelligence exploration.

The results generated by the application should not be considered a guarantee that a QR code, URL, domain, or file is completely safe or malicious.

Users should apply appropriate security practices and verify suspicious content through trusted sources.
