# data-engineering-movielens
In this project we build a data pipeline to consume data from https://www.kaggle.com/datasets/rounakbanik/the-movies-dataset?datasetId=3405 . There are cetain aspects which we will be showing. 
Setting up virtual machine and orher infra.

Prerequisites
The following requirements are needed to reproduce the project:

1. Create a GCP Project
Go to GCP console and create a project.

After you create the project, you will need to create a Service Account with the following roles:

BigQuery Admin
Storage Admin
Storage Object Admin
Viewer
Download the Service Account credentials file, rename it to google_credentials.json and store it in your home folder, in $HOME/.google/credentials/ .

IMPORTANT: if you're using a VM as recommended, you will have to upload this credentials file to the VM.

You will also need to activate the following APIs:

https://console.cloud.google.com/apis/library/iam.googleapis.com
https://console.cloud.google.com/apis/library/iamcredentials.googleapis.com


Creating a VM instance
