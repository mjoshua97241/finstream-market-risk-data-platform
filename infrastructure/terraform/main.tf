resource "google_storage_bucket" "finstream_data_lake" {
  name          = var.gcs_bucket_name
  location      = var.region
  force_destroy = true

  uniform_bucket_level_access = true

  lifecycle_rule {
    action {
      type = "Delete"
    }

    condition {
      age = 365
    }
  }
}

resource "google_bigquery_dataset" "finstream_dataset" {
  dataset_id = var.bigquery_dataset
  location   = var.region

  delete_contents_on_destroy = true
}