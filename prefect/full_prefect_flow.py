import os
import pandas as pd
from urllib import request

from prefect_gcp import GcpCredentials, GcsBucket,bigquery
from prefect_gcp.bigquery import BigQueryWarehouse

from prefect import flow,task

from make_block import create_gcp_block

res = create_gcp_block()
data_url = "https://raw.githubusercontent.com/Shivampanwar/Public_datasets/main/ratings_small.csv"

gcp_credentials = GcpCredentials.load("gcp-block")
gcs_bucket = GcsBucket(
        bucket="bucket-deproject",
        gcp_credentials=gcp_credentials
    )

gcs_bigquery =  BigQueryWarehouse(gcp_credentials=gcp_credentials)



from prefect import flow
from prefect_gcp.bigquery import GcpCredentials, BigQueryWarehouse

# @flow
# def bigquery_flow():
#     all_rows = []

#     client = gcp_credentials.get_bigquery_client()
#     client.create_dataset("test_example", exists_ok=True)

#     with BigQueryWarehouse(gcp_credentials=gcp_credentials) as warehouse:
#         warehouse.execute(
#             "CREATE TABLE IF NOT EXISTS test_example.customers (name STRING, address STRING);"
#         )
#         warehouse.execute_many(
#             "INSERT INTO test_example.customers (name, address) VALUES (%(name)s, %(address)s);",
#             seq_of_parameters=[
#                 {"name": "Marvin", "address": "Highway 42"},
#                 {"name": "Ford", "address": "Highway 42"},
#                 {"name": "Unknown", "address": "Highway 42"},
#             ],
#         )
#         while True:
#             # Repeated fetch* calls using the same operation will
#             # skip re-executing and instead return the next set of results
#             new_rows = warehouse.fetch_many("SELECT * FROM test_example.customers", size=2)
#             if len(new_rows) == 0:
#                 break
#             all_rows.extend(new_rows)
#     return all_rows

# bigquery_flow()

# from google.cloud import bigquery
# client = bigquery.Client()
# dataset_id = 'my_dataset'
    
# Configure the external data source
from google.cloud import bigquery

@task()
def bigquery_flow():
    client = gcp_credentials.get_bigquery_client()
    dataset_id = 'dataset_movie'
    project = "projectmovies-381510"
    dataset_ref = bigquery.DatasetReference(project, dataset_id)
    table_id = "movies_data"
    schema = [
        bigquery.SchemaField("userId", "STRING"),
        bigquery.SchemaField("movieId", "STRING"),
        bigquery.SchemaField("rating", "STRING"),
        bigquery.SchemaField("timestamp", "STRING"),
    ]
    # userId,movieId,rating,timestamp
    table = bigquery.Table(dataset_ref.table(table_id), schema=schema)
    # table.time_partitioning = bigquery.TimePartitioning(
    # type_=bigquery.TimePartitioningType.DAY,
    # field="timestamp",  # name of column to use for partitioning
    # expiration_ms=7776000000,
    # )  # 90 days

    # external_config = bigquery.ExternalConfig("CSV")
    external_config = bigquery.ExternalConfig("PARQUET")

    external_config.source_uris = [
        # "gs://cloud-samples-data/bigquery/us-states/us-states.csv"
        "gs://bucket-deproject/project_pth/movies_data.parquet"
    ]
    external_config.options.skip_leading_rows = 1  # optionally skip header row
    table.external_data_configuration = external_config

    # Create a permanent table linked to the GCS file
    table = client.create_table(table)  # API request
    print ("redshift table creation done ")
    return True

    # Example query to find states starting with 'W'
    # sql = 'SELECT count(*) FROM `{}.{}` WHERE name LIKE "W%"'.format(dataset_id, table_id)

    # query_job = client.query(sql)  # API request
    # print (query_job)
    # w_states = query_job  # Waits for query to finish
    # print("There are {} states with names starting with W.".format(len(w_states)))



def download_data(url):
    df = pd.read_csv(url,error_bad_lines=False)
    if os.path.exists('data'):
        pass
    else:
        os.mkdir('data')
    df.to_csv('data/movies_data.csv',index=None)
    data_pth = 'data/movies_data.csv'
    return data_pth


def transform_data(df_pth):
    df =  pd.read_csv(df_pth)
    print (df.shape)
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='s')
    for col in df.columns:
        # if col=='timestamp':
        #     pass
        # else:
        df[col] = df[col].astype(str)
    return df

@task
def write_to_parquet(url):
    '''
        url: reads from url and write to parquet 
    '''
    saved_pth =  download_data(url)
    df = transform_data(saved_pth)
    # df =  pd.read_csv(saved_pth)
    df.to_parquet(saved_pth.strip(".csv")+".parquet")

@task
def upload_to_gcs():
    
    gcs_save_pth = "project_pth/movies_data.parquet"
    gcs_bucket_path = gcs_bucket.upload_from_path(from_path='data/movies_data.parquet',to_path=gcs_save_pth)
    return gcs_bucket_path



@flow()
def cloud_storage_flow():
    # create a dummy file to upload
    write_to_parquet(data_url)
    gcs_bucket_saved_pth =  upload_to_gcs()
    print (gcs_bucket_saved_pth)
    bigquery_flow()

    
    
    


# bigquery_flow()
cloud_storage_flow()

# write_to_parquet(data_url)
# transform_data('/home/shivam/data-engineering-movielens/prefect/data/movies_data.csv')