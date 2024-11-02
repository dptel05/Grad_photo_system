import csv
import logging
from datetime import datetime
import cv2
import numpy as np
from pyzbar.pyzbar import decode

# File paths for logs and scans
CSV_FILE = 'scanned_qr_codes.csv'
LOG_FILE = 'qr_code_logger.log'

def setup_logging():
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s',
                        handlers=[logging.FileHandler(LOG_FILE), logging.StreamHandler()])

def log_qr_scan(student_id):
    with open(CSV_FILE, 'a', newline='') as file:
        csv.writer(file).writerow([student_id, datetime.now().isoformat()])
    logging.info(f"Logged QR scan: {student_id}")

def scan_qr_code():
    cap = cv2.VideoCapture(0)
    logging.info("Scanning for QR codes...")

    while True:
        ret, frame = cap.read()
        if not ret:
            logging.error("Camera error.")
            break

        for qr_code in decode(frame):
            student_id = qr_code.data.decode('utf-8')
            log_qr_scan(student_id)
            logging.info(f"Scanned QR code: {student_id}")

            # Draw a rectangle and display the student ID on the frame
            pts = [(point.x, point.y) for point in qr_code.polygon]
            cv2.polylines(frame, [np.array(pts, np.int32)], True, (0, 255, 0), 2)
            cv2.putText(frame, student_id, (qr_code.rect.left, qr_code.rect.top - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

        cv2.imshow("QR Code Scanner", frame)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    setup_logging()
    scan_qr_code()
