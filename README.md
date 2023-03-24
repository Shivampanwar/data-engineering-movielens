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

From your project's dashboard, go to Cloud Compute > VM instance
Create a new instance:
Any name of your choosing
Pick your favourite region. You can check out the regions in this link.
IMPORTANT: make sure that you use the same region for all of your Google Cloud components.

Pick a E2 series instance. A e2-standard-4 instance is recommended (4 vCPUs, 16GB RAM)
Change the boot disk to Ubuntu. The Ubuntu 20.04 LTS version is recommended. Also pick at least 30GB of storage.
Leave all other settings on their default value and click on Create.

Setting up SSH access to the VM

To SSH to your VM, generate SSH key on your local computer. Mine is Ubuntu therefore I used
ssh-keygen -t rsa -f ~/.ssh/de-zoomkey -C shivam -b 2048
Your ~/.ssh folder will now have two files namely de-zoomkey and de-zoomkey.pub for private and public part respectively. Add the public key to your project metadata in 
https://console.cloud.google.com/compute/metadata 
Following this ssh to your instance with below command.
ssh -i ~/.ssh/de-zoomkey shivam@34.131.174.70


Explain about using VS code

Now, do one thing. 
Setup GCP on machine

Upload the credentials.json file to instance and update bashrc as follows.
open bashrc like nano ~/.bashrc and add the line 
export GOOGLE_APPLICATION_CREDENTIALS="<path/to/authkeys>.json"

Exit nano with Ctrl+X. Follow the on-screen instructions to save the file and exit.
Log out of your current terminal session and log back in, or run source ~/.bashrc to activate the environment variable.

Install Gcloud  SDk copy from zitrion.
Install Gcloud from link https://cloud.google.com/sdk/docs/install for your version. 

Installing Docker 
sudo apt install docker.io
Installing Terraform
USe the link to install terraform for your setup. 
https://developer.hashicorp.com/terraform/downloads

Use the following commands to install terraform 

wget -O- https://apt.releases.hashicorp.com/gpg | gpg --dearmor | sudo tee /usr/share/keyrings/hashicorp-archive-keyring.gpg

echo "deb [signed-by=/usr/share/keyrings/hashicorp-archive-keyring.gpg] https://apt.releases.hashicorp.com $(lsb_release -cs) main" | sudo tee /etc/apt/sources.list.d/hashicorp.list

sudo apt update && sudo apt install terraform


