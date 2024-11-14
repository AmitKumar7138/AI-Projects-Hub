import logging
from data_processing import DataProcessing
from upload_code_to_s3 import upload_file_to_s3, zip_files
from config import AWS_CONFIG
import os

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    filename="ELT_log.txt",
    filemode="a",
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def main():
    data_processor = DataProcessing()
    csv_path = "Titanic-Dataset.csv"
    table_name = "TitanicData"

    data_processor.create_table_from_csv(csv_path, table_name)
    data_processor.data_preprocessing(table_name)
    data_processor.close_connection()

    # Upload code files as zip
    code_files = [
        'main.py',
        'database_connection.py',
        'data_processing.py',
        'upload_code_to_s3.py',
        # Exclude 'config.py' if necessary
    ]
    zip_name = 'code_backup.zip'
    zip_files(code_files, zip_name)

    bucket_name = AWS_CONFIG['bucket_name']
    s3_key = f"code_backup/{zip_name}"
    upload_file_to_s3(bucket_name, s3_key, zip_name)

    # Remove the zip file after uploading
    os.remove(zip_name)

if __name__ == "__main__":
    main()
