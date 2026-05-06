
## Audience Engagement Mart
Data Product for Cross-Platform Media Analytics
------------------------------
## 🎯 Overview
In a fragmented digital media ecosystem, understanding how audiences engage with content across platforms is critical. This is a Data Product designed to provide a reliable, privacy-conscious, and cost-efficient view of behavior, enabling stakeholders to monitor performance and identify optimization opportunities.
This implementation demonstrates:

* Product Management of data platforms (balancing trade-offs).
* Modern Data Engineering via a Medallion architecture (Bronze/Silver/Gold).
* Responsible Data Use through privacy-by-design and PII exclusion.

------------------------------
## 📋 Problem Statement & Strategy
Audience data is typically fragmented, expensive to process, and sensitive. This product targets marketing and editorial stakeholders who need to answer:

* How is engagement evolving over time?
* Which content categories drive the most watch time?
* Where should we prioritize editorial resources?

## Strategic Design Decisions

   1. Aggregation Level (Daily): Strategically chosen over real-time to significantly reduce infrastructure costs while still meeting weekly/monthly strategy needs.
   2. Pre-Aggregated Metrics: Sacrifices raw-event flexibility to ensure non-technical users have "instant-on" access to cthe metrics they need.
   3. Batch over Streaming: Prioritizes reliability and right-sized compute clusters for predictable cloud billing.

------------------------------
## 🚀 Technical Architecture
The pipeline follows a Lakehouse pattern, automating the movement of data from local discovery to cloud-scale visualization.

* Source: Local Parquet files (simulating cross-platform events).
** Source data: F. Maxwell Harper and Joseph A. Konstan. 2015. The MovieLens Datasets: History and Context. ACM Transactions on Interactive Intelligent Systems (TiiS) 5, 4, Article 19 (December 2015), 19 pages. DOI=<http://dx.doi.org/10.1145/2827872>
* Bronze (Storage): Raw ingestion into Google Cloud Storage (GCS).
* Silver/Gold (Warehouse): Google BigQuery utilizing an External Table strategy. This allows for a "Zero-Copy" architecture where BigQuery queries GCS directly, minimizing storage costs.
* BI Layer: Looker Studio for executive dashboards.

## 🛠️ Tech Stack

* Language: Python 3.12 (Isolated .venv).
* Cloud Platform: Google Cloud (GCP).
* Region: northamerica-northeast1 (Montreal, Canada), supposing a need for data residency compliance.
* Automation: Python google-cloud-storage SDK & GCloud CLI.

------------------------------
## 🔧 Implementation & Setup## 1. Cloud Ingestion (Python)
I developed src/cloud_storage_setup.py to automate:

* ADC Authentication: Securely linking local environments to GCP without hardcoded keys.
* Regional Provisioning: Programmatically creating buckets in Montreal.
* Automated Upload: Mapping local data_processed files to cloud blobs.

## 2. Warehousing (BigQuery)
To enable Looker Studio, I mapped the Gold-layer Parquet files to a BigQuery schema:

bq mk --external_table_definition=PARQUET=gs://[BUCKET_NAME]/*.parquet \
audience_insights_dataset.daily_engagement

------------------------------
## 🐞 Critical Debugging & Lessons Learned
Building this product required resolving several real-world infrastructure hurdles:

* Billing & Quota Management: Resolved 403 errors by programmatically linking the project to a billing account via CLI—a common hurdle in new cloud environments.
* Permission Orchestration: Fixed macOS-specific CLI conflicts in ~/.config/gcloud using ownership (chown) and permission (chmod) adjustments.
* Regional Alignment: Navigated the constraint that GCS Buckets and BigQuery Datasets must be co-located (Montreal) to prevent query execution failures.

------------------------------
## 📁 Repository Structure

├── dashboards/         # Looker Studio PDF exports/links
├── data/               # Raw source files (CSV)
├── data_processed/     # Medallion Layers (Parquet)
│   ├── bronze/         
│   ├── silver/         
│   └── gold/           # Final 'Data Product' source
├── notebooks/          # logic for transformations
├── src/                # Cloud infrastructure automation (Python)
├── requirements.txt    # Project dependencies
└── README.md

------------------------------
## 📈 Future Enhancements

* Airflow Integration: Refactor the Python ingestion and BigQuery setup into an Apache Airflow DAG for robust scheduling.
* Sentiment analysis: Integrate the tags.csv dataset to perform Sentiment Analysis on audience feedback by joining user-generated tags with engagement metrics.
* ML Foundations: Integrating engagement scoring models directly into the Silver-to-Gold transformation.



