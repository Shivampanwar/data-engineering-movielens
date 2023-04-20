# Project-data-engineering-movielens


We embarked on an exciting project to build a robust data pipeline that would consume data from a trusted source - https://www.kaggle.com/datasets/rounakbanik/the-movies-dataset?datasetId=3405.
Write objective here after dashboarding.

To kick off the process, we fetched the data from the provided URL and downloaded it onto an EC2 instance. From there, we uploaded the data to GCS, where we leveraged external tables to create new tables in BigQuery.

Thanks to the power of Prefect, we seamlessly orchestrated the entire process, while Terraform played a pivotal role in setting up the necessary infrastructure. Once we had the data securely stored, we applied transformation on the BigQuery table using DataProc in GCP. The outcome of this process was a brand new set of tables, which we used for dashboarding purposes.

In a nutshell, we were able to build a top-notch data pipeline that streamlined the entire data collection, transformation, and visualization process.
Setting up virtual machine and orher infra.
       
     
Following were the requirements for the project. 


1. Problem description
  0 points: Problem is not described
  1 point: Problem is described but shortly or not clearly
  2 points: Problem is well described and it's clear what the problem the project solves
2. Cloud
  0 points: Cloud is not used, things run only locally
  2 points: The project is developed in the cloud
  4 points: The project is developed in the cloud and IaC tools are used
3. Data ingestion (choose either batch or stream)
  Batch / Workflow orchestration
  0 points: No workflow orchestration
  2 points: Partial workflow orchestration: some steps are orchestrated, some run manually
  4 points: End-to-end pipeline: multiple steps in the DAG, uploading data to data lake
4. Data warehouse
  0 points: No DWH is used
  2 points: Tables are created in DWH, but not optimized
  4 points: Tables are partitioned and clustered in a way that makes sense for the upstream queries (with explanation)
5. Transformations (dbt, spark, etc)
  0 points: No tranformations
  2 points: Simple SQL transformation (no dbt or similar tools)
  4 points: Tranformations are defined with dbt, Spark or similar technologies
6. Dashboard
  0 points: No dashboard
  2 points: A dashboard with 1 tile
  4 points: A dashboard with 2 tiles
7. Reproducibility
  0 points: No instructions how to run code at all
  2 points: Some instructions are there, but they are not complete
  4 points: Instructions are clear, it's easy to run the code, and the code works



**Prerequisites**

The following requirements are needed to reproduce the project:

**1. Create a GCP Project**

    Go to GCP console and create a project. After you create the project, you will need to create a Service Account with the following roles:

        BigQuery Admin
        Storage Admin
        Storage Object Admin
        Viewer
        
    Download the Service Account credentials file, rename it to google_credentials.json and store it in your home folder, in $HOME/.google/credentials/ 

    IMPORTANT: if you're using a VM as recommended, you will have to upload this credentials file to the VM.

    You will also need to activate the following APIs:

    https://console.cloud.google.com/apis/library/iam.googleapis.com
    https://console.cloud.google.com/apis/library/iamcredentials.googleapis.com


**2. Creating a VM instance**

    From your project's dashboard, go to Cloud Compute > VM instance
    Create a new instance:
    Any name of your choosing
    Pick your favourite region.
    IMPORTANT: make sure that you use the same region for all of your Google Cloud components.

    Pick a E2 series instance. A e2-standard-4 instance is recommended (4 vCPUs, 16GB RAM)
    Change the boot disk to Ubuntu. The Ubuntu 20.04 LTS version is recommended. Also pick at least 30GB of storage.
    Leave all other settings on their default value and click on Create.

**3. Setting up SSH access to the VM**

    To SSH to your VM, generate SSH key on your local computer. Mine is Ubuntu therefore I used
    ssh-keygen -t rsa -f ~/.ssh/de-zoomkey -C shivam -b 2048
    Your ~/.ssh folder will now have two files namely de-zoomkey and de-zoomkey.pub for private and public part respectively. Add thebucket-deproject       public key to your project metadata in 
    https://console.cloud.google.com/compute/metadata 
    Follow this ssh to your instance with below command.
      **ssh -i ~/.ssh/de-zoomkey shivam@34.131.174.70**


Explain about using VS code

**4. Setting up GCP on the VM instance.** 

    Upload the credentials.json file  downloaded in step 1. to instance and update bashrc as follows.
    open bashrc like nano ~/.bashrc and add the line 
    export GOOGLE_APPLICATION_CREDENTIALS="<path/to/authkeys>.json"

    Exit nano with Ctrl+X. Follow the on-screen instructions to save the file and exit.
    Log out of your current terminal session and log back in, or run source ~/.bashrc to activate the environment variable.

    Install Gcloud from  [this link](/https://cloud.google.com/sdk/docs/install) for your version . 
    Download Gcloud SDK from this link and install it according to the instructions for your OS.
    Run gcloud init from a terminal and follow the instructions.
    Make sure that your project is selected with the command gcloud config list

**5. Installing docker  and terraform on the VM**
              
            1. Run sudo apt install docker.io to install it.
            2 .Change your settings so that you can run Docker without sudo:
              2.a. Run sudo groupadd docker
              2.b. Run sudo gpasswd -a $USER docker
              2.c. Log out of your SSH session and log back in.
              2.d. Run sudo service docker restart
              2.e. Test that Docker can run successfully with docker run hello-world
              
             3. Installing **Terraform**
                     Use [this link](/https://developer.hashicorp.com/terraform/downloads) to install terraform for your setup. I have anyways written                        the commands below.
              3.1. wget -O- https://apt.releases.hashicorp.com/gpg | gpg --dearmor | sudo tee /usr/share/keyrings/hashicorp-archive-keyring.gpg
              3.2. echo "deb [signed-by=/usr/share/keyrings/hashicorp-archive-keyring.gpg] https://apt.releases.hashicorp.com $(lsb_release -cs) main" | sudo tee /etc/apt/sources.list.d/hashicorp.list
              3.3.sudo apt update && sudo apt install terraform

Now, terraform is installed. 
Go to Terraform folder, execute below steps to make the obejcts.
Initialize Terraform:

**terraform init**

Plan the infrastructure and make sure that you're creating a bucket in Cloud Storage as well as a dataset in BigQuery

**terraform plan**
If the plan details are as expected, apply the changes.

**terraform apply**
Now, you should have a bucket named bucket-deproject and bigquery dataset namely dataset_movie.

Setting up ingestion flow with **prefect**


Ingestion flow is like this. We fetch data from url. Download it locally, transform it like datetime stamp. We then upload from local to GCS and then from GCS to bigquery. 




ALl code is inside the file. 

We created an external table in bigquery. Now, we will need to patition it. Therefore, we used the command 
'''
CREATE OR REPLACE TABLE projectmovies-381510.dataset_movie.movies_data_par
PARTITION BY
  DATE(datetime_column) AS

SELECT *,
  PARSE_DATETIME('%Y-%m-%d %H:%M:%S', timestamp) AS datetime_column
FROM
  projectmovies-381510.dataset_movie.movies_data;

'''

This creates a new column namely datetime_columns and we partition according to that. 


Running everytong via docker
1. Go to main project folder and run
docker build -t  project_image .
2. Run container 
docker run -p 4200:4200 project_image


Enable data proc api

