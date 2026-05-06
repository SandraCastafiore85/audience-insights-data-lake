
import os
from google.cloud import storage


def setup_gcs(bucket_name, source_file_name, destination_blob_name):
    """Creates a GCS bucket and uploads a file."""
    # Initialize the client (automatically uses your 'gcloud auth' credentials)
    storage_client = storage.Client()

    # 1. Create Bucket
    try:
        bucket = storage_client.create_bucket(bucket_name, location="northamerica-northeast1")
        print(f"Bucket {bucket.name} created.")
    except Exception as e:
        print(f"Bucket already exists or error: {e}")
        bucket = storage_client.get_bucket(bucket_name)

    # 2. Upload Parquet File
    blob = bucket.blob(destination_blob_name)
    blob.upload_from_filename(source_file_name)

    print(f"File {source_file_name} uploaded to {destination_blob_name} in {bucket_name}.")

if __name__ == "__main__":
    MY_BUCKET = 'audience_insights_data_lake_sandracastafiore_2026'
    MY_FILE = '../data/04_gold/audience_engagement_daily.parquet' 
    
    setup_gcs(MY_BUCKET, MY_FILE, "audience_engagement_daily.parquet")

