# Software Requirements Specification (SRS)

# QR Code Fraud Detection System

Version: 1.0

---

# 1. Introduction

## 1.1 Purpose

The purpose of this project is to develop a web application capable of detecting potentially fraudulent QR codes before users access malicious websites. The application will decode QR codes, analyze the embedded URLs using machine learning and security checks, and provide a risk assessment to help users avoid phishing attacks and online scams.

---

## 1.2 Problem Statement

QR codes have become widely used for payments, authentication, event registrations, restaurant menus, and product information. However, cybercriminals increasingly exploit QR codes to redirect users to phishing websites, fake payment portals, malware downloads, and credential-stealing pages.

Since users cannot visually inspect the destination of a QR code before scanning it, there is a need for an intelligent system that evaluates QR code safety before users visit the embedded link.

---

## 1.3 Scope

The application will:

- Decode QR code images.
- Extract embedded URLs.
- Analyze multiple URL security features.
- Predict whether the URL is Safe or Fraudulent.
- Display a risk score.
- Explain the prediction results.
- Store previous scan history.

Future versions will support live camera scanning, VirusTotal integration, WHOIS lookup, SSL verification, and user authentication.

---

# 2. Stakeholders

The system is intended for:

- Individual users
- Businesses
- Students
- Security researchers
- Organizations using QR codes
- Cybersecurity professionals

---

# 3. User Stories

### As a user,

I want to upload a QR code image so that I can verify whether it is safe.

### As a user,

I want to know why a QR code is considered suspicious.

### As a user,

I want to see a confidence score so I can judge the prediction reliability.

### As a user,

I want to access my previous scan history.

---

# 4. Functional Requirements

The system shall allow users to upload QR code images.

The system shall decode QR codes.

The system shall extract embedded URLs.

The system shall analyze URL security features.

The system shall classify URLs as:

- Safe
- Fraudulent

The system shall generate a confidence score.

The system shall display prediction results.

The system shall explain why a URL is considered suspicious.

The system shall store scan history.

---

# 5. Non-Functional Requirements

The application should:

- Respond within 3 seconds.
- Be easy to use.
- Support desktop and mobile devices.
- Be secure.
- Be scalable.
- Be maintainable.
- Provide reliable predictions.

---

# 6. System Features

## Feature 1

Upload QR Code

Description:

Users can upload an image containing a QR code.

---

## Feature 2

QR Code Decoding

Description:

The application extracts data embedded in the QR code.

---

## Feature 3

URL Feature Extraction

Description:

The application analyzes:

- URL length
- Domain
- HTTPS usage
- IP address usage
- URL shortening
- Number of dots
- Number of slashes
- Suspicious keywords
- Number of subdomains

---

## Feature 4

Machine Learning Prediction

Description:

The trained model predicts whether the QR code is safe or fraudulent.

---

## Feature 5

Risk Analysis

Description:

The application calculates a risk score and explains the reasons behind the prediction.

---

# 7. Assumptions

- Users upload valid QR code images.
- Internet connection is available.
- The QR code contains a URL.
- The machine learning model has been trained using quality datasets.

---

# 8. Constraints

- Version 1 only supports URL-based QR codes.
- Offline prediction may have limited functionality.
- Prediction accuracy depends on the quality of the training dataset.

---

# 9. Acceptance Criteria

The project will be considered successful if:

- QR codes can be uploaded successfully.
- QR codes are decoded correctly.
- URLs are extracted successfully.
- Machine learning predictions are generated.
- Risk scores are displayed.
- Scan history is saved.
- The user interface is responsive and user-friendly.

---

# 10. Future Enhancements

- Webcam QR scanning
- Browser extension
- Mobile application
- VirusTotal integration
- WHOIS lookup
- SSL certificate verification
- User authentication
- Admin dashboard
- PDF report generation
- Email alerts

---

# 11. Success Metrics

The project aims to achieve:

- High QR decoding accuracy
- High phishing detection accuracy
- Fast prediction time
- Responsive user interface
- Positive user experience

---

# 12. Glossary

**QR Code**  
A machine-readable code containing encoded information.

**Phishing**  
A cyberattack that tricks users into revealing sensitive information.

**Machine Learning**  
A branch of artificial intelligence that enables systems to make predictions using data.

**Risk Score**  
A numerical value representing the likelihood that a QR code is malicious.