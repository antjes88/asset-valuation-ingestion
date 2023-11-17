provider "google" {
  project = var.project_id
  region  = var.region
}

resource "google_service_account" "default" {
  account_id = var.service_account_name
  display_name = "${var.cloud_function_name} Cloud Function SA"
}

resource "google_project_iam_member" "big_query_writer" {
  project = var.project_id
  role    = "roles/bigquery.dataEditor"
  member  = "serviceAccount:${google_service_account.default.email}"
}

resource "google_project_iam_member" "big_query_jobUser" {
  project = var.project_id
  role    = "roles/bigquery.jobUser"
  member  = "serviceAccount:${google_service_account.default.email}"
}

resource "google_storage_bucket_iam_member" "binding" {
  bucket = var.storage_bucket_name
  role   = "roles/storage.objectViewer"
  member = "serviceAccount:${google_service_account.default.email}"
}


resource "google_storage_bucket" "source_code" {
  name                        = "${var.cloud_function_name}-source-code-location"
  storage_class               = "STANDARD"
  location                    = var.region
  uniform_bucket_level_access = true
}

data "archive_file" "source" {
  type        = "zip"
  source_dir  = "${path.root}/cloud_function"
  output_path = "${path.root}/zip_to_cloud_function.zip"
}

resource "google_storage_bucket_object" "zip" {
  name   = "cloud-function-source-code-for-${var.cloud_function_name}.zip"
  bucket = google_storage_bucket.source_code.name
  source = data.archive_file.source.output_path
}

resource "google_cloudfunctions_function" "default" {
  name                  = var.cloud_function_name
  runtime               = "python310"
  available_memory_mb   = 512
  timeout               = 539
  source_archive_bucket = google_storage_bucket.source_code.name
  source_archive_object = google_storage_bucket_object.zip.name
  entry_point           = var.function_entry_point
  service_account_email = google_service_account.default.email
  max_instances         = 1

  event_trigger {
    event_type = "google.storage.object.finalize"
    resource   = var.storage_bucket_name
  }
}