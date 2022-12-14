variable "aws_s3_bucket_name" {
  description = "name of s3 bucket"
  type = string
  default = "indeed-s3"
}

variable "aws_redshift_cluster_id" {
  description = "cluster id of redshift cluster"
  type = string
  default = "indeed-redshift"
}

variable "aws_redshift_db_name" {
  description = "redshift database name"
  type = string
  default = "jobs"
}

variable "aws_redshift_master_username" {
  description = "redshift master username"
  type = string
}

variable "aws_redshift_master_password" {
  description = "redshift master passsword"
  type = string
}

variable "aws_redshift_node_type" {
  description = "redshift node type"
  type = string
  default = "dc2.large"
}