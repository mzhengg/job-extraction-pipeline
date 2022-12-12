# Skills Gap Dashboard

This is an end-to-end project showcasing my skills as an aspiring Software Engineer (Data Engineer).  

Software engineering is one of the most in-demand, highest paying jobs currently. There's lots of room for growth and the industry is expected to grow by 25% through the next decade according to the Bureau of Labor Statistics (https://www.bls.gov/ooh/computer-and-information-technology/software-developers.htm). But this industry is constantly changing and new tools are being developed all the time. This project aims to track the most sought after technologies by the industry so that aspiring software engineers can keep up to date with them.  

## Technologies:

* Python (Selenium, Boto3, PySpark)
* AWS (S3, Lambda, EC2, Redshift, Elastic Beanstalk)
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

### 1) Setup Terraform
* Navigate to 'terraform' directory and follow the instructions in the Makefile - INCOMPLETE 

### 2) Test, Build, and Deploy Lambda Package
* Navigate to 'containers/lambda' directory and follow the instructions in the Makefile - INCOMPLETE

### 3) Test, Build, and Deploy Airflow Package

Airflow is used to orchestrate the web crawler. Every week, the data pipeline (containers/airflow/dags/etl.py) will scrape Indeed for new Software Engineering job postings. Each job posting will be saved as a .txt file in an S3 bucket. The S3 bucket will serve as a data lake where transformations will be performed further down the pipeline. The DAG was developed and tested on a local machine. Then, the DAG was containerized and uploaded to an AWS EC2 instance.