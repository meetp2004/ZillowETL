# Toronto Real Estate Data ETL Project
## Overview
This project aims to analyze real estate listing prices in downtown Toronto, focusing on understanding the high living costs in major cities. The project involves building an end-to-end ETL pipeline using AWS and Apache Airflow, leveraging various AWS services to extract, transform, and load data, and ultimately visualize insights using AWS QuickSight.
## Architecture
![Zillow ETL](https://github.com/meetp2004/ZillowETL/assets/65262358/ce4a7091-d8b7-4e70-bce6-4e9be06316a7)
### Components:
1. Data Extraction: Extract raw data from Zillow API using a Python script.
2. Raw Data Storage: Store raw JSON data in an S3 bucket.
3. Data Copy and Transformation:
    - Trigger AWS Lambda functions to copy raw data.
    - Transform raw JSON data into clean CSV format.
4. Data Storage: Store the transformed CSV data in another S3 bucket.
5. Query and Visualization:
    - Use AWS Athena to query the transformed data.
    - Visualize the data using AWS QuickSight.
6. Orchestration: Manage and orchestrate the entire workflow using Apache Airflow.
## Technologies Used
- AWS S3: For storing raw and transformed data.
- AWS Lambda: For serverless data transformation.
- AWS Athena: For querying the data.
- AWS QuickSight: For data visualization.
- Apache Airflow: For workflow orchestration.
- Python: For data extraction and Lambda functions.
- Terraform (Future Work): For provisioning AWS infrastructure.
- Machine Learning (Future Work): To estimate rent and home market values.

## Results
![Real Condo](https://github.com/meetp2004/ZillowETL/assets/65262358/85f00790-e81a-4aff-a67f-c905cb54effb)
![Real Single Family](https://github.com/meetp2004/ZillowETL/assets/65262358/7b88b043-2e2c-4c30-8d6f-3652b325a35b)
![Real Townhouse](https://github.com/meetp2004/ZillowETL/assets/65262358/41bc14ab-4bad-44af-98f7-0dc5a016ea2c)

