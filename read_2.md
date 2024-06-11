# Fetch Rewards Data Engineering Take Home

1. Overview

This project reads JSON data from an AWS SQS Queue, masks PII data, and writes the transformed data to a Postgres database.

2. Requirements

- Docker
- Docker-compose
- AWS CLI Local
- Postgres sql

3. Setup

1. Clone the repository.
2. Run `docker-compose up` to start Localstack and Postgres containers.
3. Run the ETL script: `python etl.py`.

4. Thought Process

1. **Read Messages from the Queue**: Used boto3 to read messages from a local instance of AWS SQS.
2. **Data Transformation**: Masked PII fields (`device_id` and `ip`) using SHA-256 hashing to ensure that data analysts can still identify duplicate values.
3. **Write to Postgres**: Inserted the transformed data into a pre-created Postgres table.

5. Next Steps

- **Error Handling**: Improve error handling and logging.
- **Testing**: Add unit tests for the ETL pipeline.
- **Scalability**: Consider batch processing for large datasets and use of an orchestration tool like Apache Airflow.

6. Deployment

In production, this application can be deployed using a container orchestration platform like Kubernetes. The following components would be essential for a production-ready solution:
- **CI/CD Pipeline**: Automate testing and deployment.
- **Monitoring**: Implement monitoring and alerting for the ETL process.
- **Secrets Management**: Securely manage database credentials and other secrets.

7. PII Recovery

To recover PII, maintain a secure mapping of original values to their masked counterparts.

8. Assumptions

- Messages in the SQS queue follow the provided JSON structure.
- The `user_logins` table in Postgres is pre-created as per the provided DDL.
