# STEDI Human Balance Analytics (Lakehouse)

## Architecture
S3 (Landing) → Glue → Trusted → Glue → Curated → ML

## Zones
- Landing: Raw JSON data
- Trusted: Filtered for consent
- Curated: ML-ready data

## Glue Jobs
- customer_landing_to_trusted
- accelerometer_landing_to_trusted
- customer_trusted_to_curated
- step_trainer_trusted
- machine_learning_curated

## How to Run
1. Upload JSON to S3 landing buckets
2. Create Glue tables using SQL
3. Run Glue jobs in order
4. Query via Athena

## Notes
- Replace YOUR_BUCKET with actual bucket
- Ensure IAM role has S3 + Glue access