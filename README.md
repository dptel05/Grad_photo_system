# Graduation Ceremony Photo Distribution System with QR Code Verification

This system automates the secure distribution of graduation photos to students using QR code verification. Each student receives only their own photo by email, ensuring privacy and ease of access.

## Project Overview

The Graduation Ceremony Photo Distribution System is designed to streamline the photo distribution process during a graduation ceremony. Using QR codes scanned on-site, the system logs each student’s ID, tags photos with this ID, and sends them directly to the student’s registered email.

## Features

1. **QR Code Scanning and Logging**: The system scans a QR code presented by each student, logs the student's ID, and timestamps each scan.
2. **Photo Tagging**: After scanning, each photo is automatically tagged with the student’s ID, making each image identifiable.
3. **Secure Email Distribution**: Only the student with a specific QR code receives their tagged photo via email, protecting their privacy.

## Modules

### 1. `qr_code.py`
   - Opens the camera and scans for QR codes.
   - Logs each valid scan with the student’s ID and a timestamp.
   - Draws a border around the detected QR code in the camera feed and displays the student ID.
   
### 2. `photo_tagging.py`
   - Continuously checks for new student IDs from the scanned log.
   - Tags the latest photo with the student’s ID.
   - Copies each tagged photo to a secure output directory.

### 3. `email_sender.py`
   - Reads student emails and IDs from a CSV file.
   - Sends each tagged photo to the corresponding student via email.
   - Verifies photo existence before sending to ensure no photo is missed.

## Requirements

- Python 3.x
- OpenCV
- pyzbar
- pandas
- smtplib (for secure email transmission)

## Usage

1. Run `qr_code.py` to start scanning students’ QR codes.
2. Run `photo_tagging.py` to tag and organize photos by student ID.
3. Run `email_sender.py` to distribute tagged photos via email.

## Installation

1. Clone this repository.
2. Install the dependencies using:
   ```bash
   pip install -r requirements.txt
