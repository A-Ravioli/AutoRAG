# The Internal Tooling to RAG and setup SLMs and LLMs for companies

## Local Deployment

``` sh
#!/bin/bash

docker build -t rag_system .
docker run -d -p 5000:5000 rag_system
```

## AWS Deployment

``` sh
#!/bin/bash

# AWS CLI commands to push Docker image to ECR and deploy to ECS
# Ensure you have AWS CLI configured with necessary permissions

# Replace with your AWS details
AWS_ACCOUNT_ID=your_account_id
AWS_REGION=your_region
ECR_REPOSITORY=your_repository_name

$(aws ecr get-login --no-include-email --region $AWS_REGION)

docker build -t rag_system .
docker tag rag_system:latest $AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/$ECR_REPOSITORY:latest
docker push $AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/$ECR_REPOSITORY:latest

# Deploy to ECS (details depend on your ECS setup)
# Example:
aws ecs update-service --cluster your_cluster_name --service your_service_name --force-new-deployment
```

## Google Cloud Deployment

``` sh
#!/bin/bash

# Google Cloud SDK commands to push Docker image to GCR and deploy to GKE
# Ensure you have gcloud CLI configured with necessary permissions

# Replace with your GCP details
GCP_PROJECT_ID=your_project_id
GCR_REPOSITORY=your_repository_name

gcloud auth configure-docker

docker build -t gcr.io/$GCP_PROJECT_ID/$GCR_REPOSITORY:latest .
docker push gcr.io/$GCP_PROJECT_ID/$GCR_REPOSITORY:latest

# Deploy to GKE (details depend on your GKE setup)
# Example:
kubectl set image deployment/your_deployment_name your_container_name=gcr.io/$GCP_PROJECT_ID/$GCR_REPOSITORY:latest
```
