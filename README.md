# End to End Data Science Project

### Workflows--ML Pipeline

1. Data Ingestion
2. Data Validation
3. Data Transformation-- Feature Engineering,Data Preprocessing
4. Model Trainer
5. Model Evaluation- MLFLOW,Dagshub

## Workflows

1. Update config.yaml
2. Update schema.yaml
3. Update params.yaml
4. Update the entity
5. Update the configuration manager in src config
6. Update the components
7. Update the pipeline 
8. Update the main.py


# Docker steps


docker login -u subbaraogadamsetty

dckr_pat_OKcIBCezgIgvSlpzDSiUx_A8tOg

> Create EC2 instance + generate key value pairs

	ec2-54-159-123-180.compute-1.amazonaws.com

> Generate new token in docker (

> Go to git-hub project and create EC2_SSH_KEY using californiahousingkeypair.pem
SubbaRao-Gadamsetty
datascienseproject


chmod 400 californiahousingkeypair.pem

docker build -t california-api .
docker tag california-api subbaraogadamsetty/california-api:latest
docker login
docker push subbaraogadamsetty/california-api:latest

ssh -i californiahousingkeypair.pem ec2-54-159-123-180.compute-1.amazonaws.com
docker pull subbaraogadamsetty/california-api:latest
docker run -d -p 8080:8080 --name california-api subbaraogadamsetty/california-api:latest
