import time
import shutil
import logging
import pandas as pd
from pathlib import Path

PHOTO_DIR = "captured_photos/"
OUTPUT_DIR = "tagged_photos/"
CSV_FILE = 'scanned_qr_codes.csv'  # CSV where each scanned student_id is recorded
SCAN_INTERVAL = 1.0

class PhotoTagger:
    def __init__(self, photo_dir: str, output_dir: str, csv_file: str):
        self.photo_dir = Path(photo_dir)
        self.output_dir = Path(output_dir)
        self.csv_file = csv_file
        self.processed_ids = set()
        self._setup_logging()
        self._create_directories()

    def _setup_logging(self):
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[logging.FileHandler('photo_tagger.log'), logging.StreamHandler()]
        )

    def _create_directories(self):
        for directory in [self.photo_dir, self.output_dir]:
            directory.mkdir(parents=True, exist_ok=True)
            logging.info(f"Ensured directory exists: {directory}")

    def load_new_student_ids(self):
        """Load unprocessed student IDs from the CSV file."""
        try:
            data = pd.read_csv(self.csv_file)
            all_ids = set(data['student_id'].astype(str))
            new_ids = all_ids - self.processed_ids
            self.processed_ids.update(new_ids)
            return list(new_ids)
        except Exception as e:
            logging.error(f"Error loading student IDs from {self.csv_file}: {e}")
            return []

    def copy_photo_with_student_id(self, student_id: str) -> bool:
        """Find the latest photo and copy it using the student ID."""
        photos = sorted(self.photo_dir.glob("*.jpg"), key=lambda p: p.stat().st_mtime, reverse=True)
        if photos:
            latest_photo = photos[0]
            new_filename = f"{student_id}.jpg"
            new_path = self.output_dir / new_filename
            shutil.copy(str(latest_photo), str(new_path))  # Copy instead of move
            logging.info(f"Copied {latest_photo.name} to {new_filename}")
            return True
        logging.warning("No new photos to copy.")
        return False

    def process_photos(self):
        """Rename photos based on new student IDs found in CSV."""
        new_student_ids = self.load_new_student_ids()
        for student_id in new_student_ids:
            logging.info(f"Processing student ID: {student_id}")
            for _ in range(10):  # Retry mechanism to wait for the photo capture
                if self.copy_photo_with_student_id(student_id):
                    break
                logging.info("Waiting for photo capture...")
                time.sleep(SCAN_INTERVAL)

if __name__ == "__main__":
    tagger = PhotoTagger(PHOTO_DIR, OUTPUT_DIR, CSV_FILE)
    while True:
        tagger.process_photos()
        time.sleep(2)  # Interval between sessions
