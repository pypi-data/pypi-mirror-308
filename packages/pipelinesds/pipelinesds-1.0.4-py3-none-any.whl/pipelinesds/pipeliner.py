from google.cloud import bigquery, bigquery_storage, storage
import pickle
import pandas as pd

def get_results_from_bq(bq_client,bq_storage_client,table,where_clause=None):
    """
    Returns SQL results from BigQuery as dataframe.

    Parameters
    ----------
    bq_client: google.cloud.bigquery.Client
        BigQuery client.
    bq_storage_client: google.cloud.bigquery_storage.BigQueryReadClient
        BigQuery Storage client.
    table: str
        Name of table/view to get data from.
    where_clause: str
        Where clause to filter data.

    Returns
    ----------
    pd.DataFrame
        Data from the view/table.
    """
    sql = f"""
     SELECT * FROM `{table}` {where_clause}
    """
    
    results = bq_client.query(sql).to_dataframe(bqstorage_client=bq_storage_client)
    return results

def delete_old_data(bq_client,table, where_clause):
    """
    Delete old data from BigQuery table.

    Parameters
    ----------
    bq_client: google.cloud.bigquery.Client
        BigQuery client.
    bq_storage_client: google.cloud.bigquery_storage.BigQueryReadClient
        BigQuery Storage client.
    table: str
        Name of table/view to delete data from.
    where_clause: str
        Where clause to filter data.
    """
    
    sql = f"""
    DELETE FROM `{table}`WHERE {where_clause}
    """
    bq_client.query(sql).result()

def write_dataframe_to_bq(bq_client,df, table_id, write_disposition, job_config):
    """
    Function to write dataframe to BigQuery table

    Parameters
    ----------
    bq_client: google.cloud.bigquery.Client
        BigQuery client.
    df: pd.DataFrame
        Dataframe to write
    table_id: string
        Table in BigQuery to write dataframe
    write_disposition : str
        Type of write results (either 'WRITE_APPEND', 'WRITE_TRUNCATE' or 'WRITE_EMPTY').
    """
    job = bq_client.load_table_from_dataframe(
        df,
        table_id,
        job_config=job_config
    )
    job.result()

def read_gcs_file(gcs_client,bucket_name, destination_blob_name):
    """
    Function to read a file from a specific path on Google Cloud Storage.
        
    Parameters
    ----------
    gcs_client: google.cloud.storage.Client
        Google Cloud Storage client.
    bucket_name: str
        Name of bucket on GCS, where file is written.
    destination_blob_name: str
        Path in bucket to read file.

    Returns
    ----------
    object
        The object read from the file.
    """
    bucket = gcs_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    file = pickle.load(blob.open(mode='rb'))
    return file

def save_gcs_file(gcs_client,bucket_name, destination_blob_name, content, content_type):
    """
    Function to save content to a specific path on Google Cloud Storage.
    
    Parameters
    ----------
    gcs_client: google.cloud.storage.Client
        Google Cloud Storage client.
    bucket_name: str
        Name of the bucket on GCS where the file will be saved.
    destination_blob_name: str
        Path in the bucket to save the file.
    content: str
        The content to be saved.
    content_type: str
        The MIME type of the content (eg. 'text/html' or 'application/json').
    """
    bucket = gcs_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    blob.upload_from_string(content, content_type=content_type)