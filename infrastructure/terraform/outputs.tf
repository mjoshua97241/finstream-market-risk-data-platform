output "data_lake_bucket" {
  value = google_storage_bucket.finstream_data_lake
}

output "bigquery_dataset" {
  value = google_bigquery_dataset.finstream_dataset
}