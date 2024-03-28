import csv
from google.cloud import bigquery
import os

#Set your Google Cloud credentials
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "service-account.json"

#Function to generate NBA schema from the CSV file
def generate_schema_from_csv(csv_path):
    column_types = {
        "YEAR": "STRING",
        "TEAM": "STRING",
        "W": "INTEGER",
        "L": "INTEGER",
    }
    with open(csv_path, newline='') as csvfile:
        reader = csv.reader(csvfile)
        headers = next(reader)

        #Adjust header names as needed
        headers = ['YEAR' if header == 'SEASON' else header for header in headers]
        headers = ['TEAM' if header == 'TEAM_NAME' else header for header in headers]

    schema = []
    for header in headers:
        #Ensure header adjustments are reflected in schema
        data_type = column_types.get(header, "FLOAT")  # Default to FLOAT if not explicitly mapped
        schema.append(bigquery.SchemaField(header, data_type))
    return schema

#Function to create a dataset and table in BigQuery
def create_bigquery_dataset_and_table(dataset_name, table_name, csv_path):
    client = bigquery.Client()
    schema = generate_schema_from_csv(csv_path)

    #Create dataset
    dataset_id = f"{client.project}.{dataset_name}"
    dataset = bigquery.Dataset(dataset_id)
    dataset.location = "US"
    client.create_dataset(dataset, exists_ok=True)

    #Create table with the generated schema
    table_id = f"{dataset_id}.{table_name}"
    table = bigquery.Table(table_id, schema=schema)
    client.create_table(table, exists_ok=True)
    print(f"Table {table_id} created with the generated schema.")

#Function to load the CSV data into the BigQuery table
def load_csv_to_bigquery(dataset_name, table_name, csv_file_path):
    client = bigquery.Client()
    table_id = f"{client.project}.{dataset_name}.{table_name}"

    job_config = bigquery.LoadJobConfig(
        source_format=bigquery.SourceFormat.CSV,
        skip_leading_rows=1,
        autodetect=False,
        schema=generate_schema_from_csv(csv_file_path)
    )

    with open(csv_file_path, "rb") as source_file:
        job = client.load_table_from_file(source_file, table_id, job_config=job_config)
    job.result()
    print(f"Loaded {job.output_rows} rows into {table_id}.")

#Creation of the BigQuery schema, dataset, table, and data loading
def main(csv_file_path, dataset_name, table_name):
    create_bigquery_dataset_and_table(dataset_name, table_name, csv_file_path)
    load_csv_to_bigquery(dataset_name, table_name, csv_file_path)

if __name__ == "__main__":
    csv_file_path = "/Users/Omar.Hakawati/Desktop/nbaStats/nba_team_data.csv"  #Update this path to your CSV file
    dataset_name = "nba_ds"
    table_name = "nba_teams_tb"  #Updated table name
    main(csv_file_path, dataset_name, table_name)
