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


### MLFLOW On AWS
## MLflow on AWS Setup:

1. Login to AWS console.
2. Create IAM user with AdministratorAccess
	mlflowuser
		Access key: AKIATD3BCFM6MKP462CG
		Secret access key: 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
	datascienseuser
		Access key: AKIATD3BCFM6HNMB5FFT
		Secret access key: nvg+oRfTAMRXH24zMIrLQbTnNMM0tLBlUHPwT83w
		Default region name: us-east-1

3. Export the credentials in your AWS CLI by running "aws configure"
	install AWS CLI
	Go to venv and execute aws configure

4. Create a s3 bucket
	datasciensebuket
5. Create EC2 machine (Ubuntu) + add Security groups 5000 port + connect
	datascienseEC2
	datascienseKeyPair
	Public IPv4 address: 52.207.64.161
	Public DNS: ec2-52-207-64-161.compute-1.amazonaws.com
	EC2 Instance Connect
		bash prompt will be opened with ubuntu

Run the following command on EC2 machine
```bash

################## INSTALLATION OF MLFLOW (First time) #########################
sudo apt update

sudo apt install python3-pip

sudo apt install pipenv

sudo apt install virtualenv

mkdir mlflow

cd mlflow

pipenv install mlflow

pipenv install awscli

pipenv install boto3

pipenv shell

mlflow --version

pip show boto3

## Then set aws credentials
aws configure

	datascienseuser
		Access key: AKIATD3BCFM6HNMB5FFT
		Secret access key: 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
		Default region name: us-east-1

mlflow server \
  --host 0.0.0.0 \
  --port 5000 \
  --default-artifact-root s3://datasciensebuket

#open Public IPv4 DNS to the port 5000


#set uri in your local terminal and in your code 
export MLFLOW_TRACKING_URI=http://ec2-52-207-64-161.compute-1.amazonaws.com:5000/

################ ONLY RUNNING MLFLOW ################

cd mlflow

pipenv shell

mlflow --version

pip show boto3


mlflow server \
  --host 0.0.0.0 \
  --port 5000 \
  --default-artifact-root s3://datasciensebuket
  
export MLFLOW_TRACKING_URI=http://ec2-98-83-134-83.compute-1.amazonaws.com:5000/


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
