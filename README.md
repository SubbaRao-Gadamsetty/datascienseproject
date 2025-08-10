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

3. Export the credentials in your AWS CLI by running "aws configure"
	install AWS CLI
	Go to venv and execute aws configure

4. Create a s3 bucket
	datasciensebuket
5. Create EC2 machine (Ubuntu) + add Security groups 5000 port + connect
	datascienseEC2
	datascienseKeyPair
	Public IPv4 address: 52.207.64.161
	Public DNS: ec2-52-55-105-249.compute-1.amazonaws.com
	EC2 Instance Connect
		bash prompt will be opened with ubuntu

	ECR:
		214415059772.dkr.ecr.us-east-1.amazonaws.com/datascienseecr

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
aws configure list
aws configure


mlflow server \
  --host 0.0.0.0 \
  --port 5000 \
  --default-artifact-root s3://datasciensebuket

#open Public IPv4 DNS to the port 5000


#set uri in your local terminal and in your code 
export MLFLOW_TRACKING_URI=http://ec2-52-55-105-249.compute-1.amazonaws.com:5000/

###################################


ONLY FOR REF
export MLFLOW_TRACKING_URI=http://ec2-52-55-105-249.compute-1.amazonaws.com:5000/

## Docker Setup In EC2 commands to be Executed

#optinal

sudo apt-get update -y

sudo apt-get upgrade

#required

curl -fsSL https://get.docker.com -o get-docker.sh

sudo sh get-docker.sh

sudo usermod -aG docker ubuntu

newgrp docker

## Github - Self-hosted runner

mkdir actions-runner && cd actions-runner

curl -o actions-runner-linux-x64-2.327.1.tar.gz -L https://github.com/actions/runner/releases/download/v2.327.1/actions-runner-linux-x64-2.327.1.tar.gz

echo "d68ac1f500b747d1271d9e52661c408d56cffd226974f68b7dc813e30b9e0575  actions-runner-linux-x64-2.327.1.tar.gz" | shasum -a 256 -c

tar xzf ./actions-runner-linux-x64-2.327.1.tar.gz

./config.sh --url https://github.com/SubbaRao-Gadamsetty/datascienseproject --token BVDPZJJWCTG4QSK6TB23EX3ITCIY4

# Enter the name of runner : [self-hosted]
./run.sh

## Configure EC2 as self-hosted runner:

## Setup github secrets:

AWS_ACCESS_KEY_ID=

AWS_SECRET_ACCESS_KEY=

AWS_REGION = us-east-1

AWS_ECR_LOGIN_URI = demo>>  214415059772.dkr.ecr.us-east-1.amazonaws.com/datascienseecr

ECR_REPOSITORY_NAME = datascienseecr



################ ONLY RUNNING MLFLOW (SECOND TIME) ################

cd mlflow

pipenv shell

mlflow --version

pip show boto3

aws s3 ls

mlflow server \
  --host 0.0.0.0 \
  --port 5000 \
  --default-artifact-root s3://datasciensebuket
  

################ ECR  SECOND TIME ################
docker --version
docker ps

ls -la ~/actions-runner
cd ~/actions-runner
./run.sh


-----
ECR
-----
	214415059772.dkr.ecr.us-east-1.amazonaws.com/datascienseproject

-----
EC2
-----
	datasciensewebserver
		IPV4
			52.203.118.11
		PUBLIC DNS
			ec2-52-203-118-11.compute-1.amazonaws.com
		datascienseKeyPair.pem











#### Below steps are for backup and should be removed later
# Docker steps


docker login -u subbaraogadamsetty

dckr_pat_OKcIBCezgIgvSlpzDSiUx_A8tOg

> Create EC2 instance + generate key value pairs

	ec2-52-55-105-249.compute-1.amazonaws.com

> Generate new token in docker (

> Go to git-hub project and create EC2_SSH_KEY using californiahousingkeypair.pem
SubbaRao-Gadamsetty
datascienseproject


chmod 400 californiahousingkeypair.pem

docker build -t california-api .
docker tag california-api subbaraogadamsetty/california-api:latest
docker login
docker push subbaraogadamsetty/california-api:latest

ssh -i californiahousingkeypair.pem ec2-52-55-105-249.compute-1.amazonaws.com
docker pull subbaraogadamsetty/california-api:latest
docker run -d -p 8080:8080 --name california-api subbaraogadamsetty/california-api:latest
