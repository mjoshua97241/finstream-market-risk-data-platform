variable "project_id" {
  description = "GCP project id"
  type = string
}

variable "region" {
  description = "GCP region"
  default = "us-central1"
}

variable "gcs_bucket_name" {
  description = "Data lake bucket name"
  type = string
}

variable "bigquery_dataset" {
  description = "BigQuery dataset name"
  default = "finstream_dw"
}