terraform {
  required_version = ">= 1.0"
  backend "gcs" {
    bucket = "terraform-state-v8q0qvfi"
    prefix = "terraform/state/asset-valuation-ingestion"
  }

  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 5.0"
    }
  }
}

provider "google" {
  project = var.project_id
  region  = var.region
}

resource "time_static" "build_time" {}

locals {
  temp_folder_name        = "${var.temp_folder_prefix}-${replace(time_static.build_time.rfc3339, "/[-:TZ]/", "")}"
  zip_file_local_path     = "./zip_to_cloud_function.zip"
  bucket_object_file_path = "${var.cloud_function_name}/source-code-${replace(time_static.build_time.rfc3339, "/[-:TZ]/", "")}.zip"
}


# zip the source code and upload it to the bucket
data "google_storage_bucket" "source_code" {
  name = "source-code-cloud-functions-cyd2y7j6"
}

resource "google_storage_bucket_object" "zip_file" {
  name   = local.bucket_object_file_path
  bucket = data.google_storage_bucket.source_code.name
  source = var.zip_file_path
}

# Creation of triggering bucket
resource "google_storage_bucket" "raw_assets" {
  name                        = "assets-collection-raw-ckd2y1t6"
  storage_class               = "STANDARD"
  location                    = var.region
  uniform_bucket_level_access = true
  force_destroy               = false
}

# Creation of Service Account
resource "google_service_account" "default" {
  account_id   = var.service_account_name
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

resource "google_project_iam_member" "run_invoker" {
  project = var.project_id
  role    = "roles/run.invoker"
  member  = "serviceAccount:${google_service_account.default.email}"
}

resource "google_project_iam_member" "eventarc_event_receiver" {
  project = var.project_id
  role    = "roles/eventarc.eventReceiver"
  member  = "serviceAccount:${google_service_account.default.email}"
}

resource "google_storage_bucket_iam_member" "storage_viewer" {
  bucket = google_storage_bucket.raw_assets.name
  role   = "roles/storage.objectViewer"
  member = "serviceAccount:${google_service_account.default.email}"
}


# Creation of the Cloud Function
resource "google_cloudfunctions2_function" "default" {
  name     = var.cloud_function_name
  location = var.region

  build_config {
    runtime     = "python310"
    entry_point = var.function_entry_point
    source {
      storage_source {
        bucket = data.google_storage_bucket.source_code.name
        object = google_storage_bucket_object.zip_file.name
      }
    }
  }

  service_config {
    available_memory      = "512M"
    timeout_seconds       = 539
    max_instance_count    = 1
    service_account_email = google_service_account.default.email
  }

  event_trigger {
    trigger_region        = var.region
    event_type            = "google.cloud.storage.object.v1.finalized"
    service_account_email = google_service_account.default.email
    event_filters {
      attribute = "bucket"
      value     = google_storage_bucket.raw_assets.name
    }
  }
  depends_on = [
    google_project_iam_member.run_invoker,
    google_project_iam_member.eventarc_event_receiver
  ]
}
