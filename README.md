# Malicious App Permission Analyzer

A web-based security tool that analyzes Android APK permissions and identifies potentially risky permissions.

## Project Overview

Malicious App Permission Analyzer helps users understand the security and privacy risks of an Android application by analyzing the permissions requested by an APK file.

The system extracts permissions from the Android Manifest and calculates a risk score based on predefined permission risk levels.

## Key Features

- Upload Android APK files
- Extract APK permissions
- Analyze risky permissions
- Calculate security risk score
- Display Low, Medium, or High Risk
- Show high-risk and medium-risk permissions
- Simple and user-friendly interface

## How It Works

1. Upload an APK file
2. Extract permissions from AndroidManifest
3. Compare permissions with predefined risk levels
4. Calculate the risk score
5. Display the security analysis report

## Technologies Used

- Python
- Flask
- HTML
- CSS
- APK Permission Analysis
- GitHub

## Risk Levels

- **LOW RISK** – Few or no sensitive permissions detected
- **MEDIUM RISK** – Some potentially sensitive permissions detected
- **HIGH RISK** – Multiple high-risk permissions detected

## Project Limitation

This project performs permission-based risk analysis. It is not a complete malware detection system.

## Future Enhancements

- Machine Learning based malware detection
- Permission behavior analysis
- App reputation checking
- Malware database integration
- Detailed security reports

## Project Expo 2026

**Course:** B.E. CSE (Cyber Security)  
**Project:** Malicious App Permission Analyzer  
**Type:** Software Project
