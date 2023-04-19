terraform {
  required_providers {
    google = {
      source = "hashicorp/google"
      version = "4.51.0"
    }
  }
}

provider "google" {
  credentials = file("/home/shivam/gcp_creds/gcp_cred.json")

  project = "projectmovies-381510"
  region  = "asia-south2"
  zone    = "asia-south2-a"
}




resource "google_storage_bucket" "static" {
  name          = "bucket-deproject"
  location      = "ASIA-SOUTH2"

  uniform_bucket_level_access = true
  
storage_class = "STANDARD"

force_destroy = true


  lifecycle_rule {
    action {
      type = "Delete"
    }
    condition {
      age = 30  // days
    }
  }


  
}


resource "google_bigquery_dataset" "dataset" {
  dataset_id ="dataset_movie"
  project   = "projectmovies-381510"
  location      = "asia-south2"
}