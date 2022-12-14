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
  bucket = "mzheng-${var.aws_s3_bucket_name}"
}

# create redshift cluster
resource "aws_redshift_cluster" "data-warehouse" {
  cluster_identifier = "mzheng-${var.aws_redshift_cluster_id}"
  database_name      = "${aws_redshift_db_name}"
  master_username    = "${aws_redshift_master_username}"
  master_password    = "${aws_redshift_master_password}"
  node_type          = "${aws_redshift_node_type}"
}