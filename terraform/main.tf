terraform {
  required_providers {
    aws = {
      source = "hashicorp/aws"
      version = "~> 4.16"
    }
  }

  required_version = ">= 1.2.0"
}

provider "aws" {
  region = "us-west-2"
}

# create S3 bucket
resource "aws_s3_bucket" "data-lake" {
  bucket = "${var.aws_s3_bucket_name}"
}

# create redshift cluster
resource "aws_redshift_cluster" "data-warehouse" {
  cluster_identifier = "${var.aws_redshift_cluster_id}"
  database_name      = "${var.aws_redshift_db_name}"
  master_username    = "${var.aws_redshift_master_username}"
  master_password    = "${var.aws_redshift_master_password}"
  node_type          = "${var.aws_redshift_node_type}"

  # to ensure succesful destroy
  skip_final_snapshot = true
}