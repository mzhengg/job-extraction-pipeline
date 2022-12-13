# Job Extraction Pipeline

Software engineering is one of the most in-demand, highest paying jobs currently. There's lots of room for growth and the industry is expected to grow by 25% through the next decade according to the Bureau of Labor Statistics (https://www.bls.gov/ooh/computer-and-information-technology/software-developers.htm). But this industry is constantly changing and new positions are opening up all the time. This project aims to track the number of positions open for the various specialities within software engineering so that aspiring software engineers can pivot into growing fields, learn the necessary skills, and get a job with a good growth outlook.

## Technologies:

* Python (Selenium, Boto3, PySpark)
* AWS (S3, Fargate, MWAA, Redshift)
* Airflow
* Docker
* Terraform

![My_Image](diagram.jpg)

## Overview of Terraform

An infrastructure-as-code (the process of managing and provisioning computer data centers through code instead of manual processes) tool that lets you define both cloud and on-premise resources in human-readable configuration files that you can version, reuse, and share. You can then use a consistent workflow to provision and manage all of your infrastructure throughout its lifecycle.

## Overview of Docker

Docker is a platform that enables developers to build, deploy, run, update, and manage containers.  

Containers: package of software that includes everything needed to run an application: code, dependencies, etc.  

Containers are isolated from each other and can be ran in different environments (Windows, macOS, GCP, etc.)  

Allows:
* Reproducibility 
* Local experiments 
* Integration testing 
* Running pipelines on the cloud 
* The use of Spark 
* Serverless computing 

Dockerfile: a text file you create that builds a Docker image  

Docker image: a file containing instructions to build a Docker container  

Docker container: a running instance of a Docker image
* Since a Docker image is just a snapshot, any modifications performed in the container will be lost upon restarting the container  

Dockerfile -> (Build) -> Docker image -> (Run) -> Docker container  

Docker compose (docker-compose.yml): a file to deploy, combine, and configure many Docker images at once  

Docker volume: file system mounted on Docker container to preserve data generated by the running container (stored on the host, independent of the container life cycle  

“Docker rule” is to outsource every process to its own container  

## Overview of Airflow

Apache Airflow is the most popular data workflow orchestration tool.   

## How to Setup and Deploy Dashboard

### 1) Setup Infrastucture using Terraform

Terraform is used to set up the AWS infrastructure.  

#### Steps

1. Get AWS keys by following these steps:
    - sign into AWS console
    - click on username
    - click on security credentials
    - create access key

2. Set these environment variables (these are dummy keys, replace them with your own before executing):

```bash
export AWS_ACCESS_KEY_ID=AKIAIOSFODNN7EXAMPLE
export AWS_SECRET_ACCESS_KEY=wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY  
```

3. Build infrastructure by executing these commands in order:
```bash
terraform init
```
```bash
terraform plan
```
```bash
terraform apply
```

4. Destroy the infrastructure (when they are no longer needed):
```bash
terraform destroy
```

### 2) Test and Deploy Container to AWS Fargate

AWS Fargate is used to host and execute a container that will:
    - Scrape Indeed.com using Selenium and Python
    - Upload the raw job postings to AWS S3
    - Transform the raw data using PySpark
    - Store the structured data in AWS Redshift  

By default, the script only scrapes one type of job: Software Engineer. In the future, there is room to scrape other jobs as well! But for now, we will scrape 20 pages of that one job every week.  

At first, I intended to use AWS Lambda to trigger the pipeline to run. However, I realized this wasn't necessary and it only added an extra layer of complexity. I encountered a lot of difficulty running headless Chrome in a container. After days of searching, I stumbled across this repo: https://github.com/umihico/docker-selenium-lambda. The repo provides a Dockerfile that builds a container that runs Chrome using the AWS Lambda RIE (Runtime Interface Emulator). Even though I won't be using AWS Lambda, this Dockerfile provides a convenient way to Dockerize my selenium web crawler for deployment to AWS Fargate.

#### Steps

1. Build the image:
```bash
docker build . \
	--tag scraper:latest
```

2. Run the image (these are dummy keys, replace them with your own before executing)
```bash
docker run \
    -p 9000:8080 \
    --name scraper \
    -e AWS_ACCESS_KEY_ID=AKIAIOSFODNN7EXAMPLE \
    -e AWS_SECRET_ACCESS_KEY=wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY \
    -e AWS_DEFAULT_REGION=us-west-2 \
    scraper:latest
```

3. Delete the image and container (when they are no longer needed)
```bash
docker kill scraper
docker rm scraper
docker image rm scraper:latest
```

### 3) Test and Deploy Airflow DAG to AWS MWAA

Airflow is used to orchestrate the lambda function. Every week, the DAG will trigger the data pipeline to scrape Indeed for new Software Engineering job postings. Each job posting will be saved as a .txt file in an S3 bucket. The S3 bucket will serve as a data lake. Then the raw data will be transformed using PySpark and uploaded to AWS Redshift. The DAG was developed and tested on a local machine using https://github.com/aws/aws-mwaa-local-runner. Then, the DAG was deployed to AWS MWAA.

#### Steps

1. Build the Docker container image using the following command:
```bash
./mwaa-local-env build-image
```

2. Runs a local Apache Airflow environment that is a close representation of MWAA by configuration.
```bash
./mwaa-local-env start
```

*To stop the local environment, Ctrl+C on the terminal and wait until the local runner and the postgres containers are stopped.*

3. Access the Airflow UI

By default, the `bootstrap.sh` script creates a username and password for your local Airflow environment.

- Username: `admin`
- Password: `test`
- Open the Apache Airlfow UI: <http://localhost:8080/>.

4. Add DAGs and supporting files

- Add DAG code to the `dags/` folder.
- Add Python dependencies to `requirements/requirements.txt`.
    * To test a requirements.txt without running Apache Airflow, use the following script:
    ```bash
    ./mwaa-local-env test-requirements
    ```
- Add custom plugins to the `plugins/` folder.