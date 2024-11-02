import smtplib
import pandas as pd
from email.message import EmailMessage
from pathlib import Path
import logging

# Configuration
CSV_FILE = 'student_emails.csv'
OUTPUT_DIR = "tagged_photos/"
SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 465
EMAIL_ADDRESS = 'dhruvpt3408@gmail.com'
EMAIL_PASSWORD = 'xjvy ykpn kwch gtre'

def send_photos():
    # Setup logging
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    # Load student emails from CSV
    try:
        email_data = pd.read_csv(CSV_FILE)
    except Exception as e:
        logging.error(f"Could not load CSV file {CSV_FILE}: {e}")
        return

    # Iterate through each student and email
    for _, row in email_data.iterrows():
        student_id = str(row['student_id'])
        to_email = row['email']
        photo_path = Path(OUTPUT_DIR) / f"{student_id}.jpg"

        # Check if photo exists
        if not photo_path.exists():
            logging.warning(f"Photo not found for student ID {student_id}")
            continue

        # Create and send email
        msg = EmailMessage()
        msg['Subject'] = 'Your Graduation Photo'
        msg['From'] = EMAIL_ADDRESS
        msg['To'] = to_email
        msg.set_content(f"Dear Student {student_id},\n\nCongratulations on your graduation! Please find attached your graduation photo.\n\nBest regards,\nUniversity Team")

        # Attach photo and send
        with open(photo_path, 'rb') as f:
            msg.add_attachment(f.read(), maintype='image', subtype='jpeg', filename=f"{student_id}.jpg")

        try:
            with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT) as smtp:
                smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
                smtp.send_message(msg)
                logging.info(f"Email sent to {to_email} for student ID {student_id}")
        except Exception as e:
            logging.error(f"Failed to send email to {to_email} for student ID {student_id}: {e}")

if __name__ == "__main__":
    send_photos()
