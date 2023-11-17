variable "project_id" {
  type        = string
  description = "Name of the Google Project"
}

variable "region" {
  type        = string
  default     = "europe-west2"
  description = "Location for the resources"
}

variable "cloud_function_name" {
  type        = string
  description = "Name of the CSV Ingestion Cloud Function"
}

variable "function_entry_point" {
  type        = string
  default     = "function_entry_point"
  description = "Name of the function entry point for the Python solution at main.py"
}

variable "service_account_name" {
  type        = string
  description = "Name of the Service Account"
}

variable "storage_bucket_name" {
  type        = string
  description = "Name of the Trigger bucket name"
}