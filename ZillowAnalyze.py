from airflow import DAG
from datetime import timedelta, datetime
from airflow.operators.python import PythonOperator
from airflow.operators.bash_operator import BashOperator
from airflow.providers.amazon.aws.sensors.s3 import S3KeySensor
import json
import requests


with open('/home/ubuntu/airflow/config_api.json', 'r') as config_file:
    api_host_key = json.load(config_file)

now = datetime.now()
dt_now_string = now.strftime("%d%m%Y%H%M%S")
s3_bucket = 'required-data-csv-bucket'
def extract_zillow_data(**kwargs):
    url = kwargs['url']
    headers = kwargs['headers']
    querystring = kwargs['querystring']
    dt_string = kwargs['date_string']
    # return headers
    response = requests.get(url, headers=headers, params=querystring)
    response_data = response.json()
    

    # Specify the output file path
    output_file_path = f"/home/ubuntu/response_data_{dt_string}.json"
    print(output_file_path)
    file_str = f'response_data_{dt_string}.csv'

    # Write the JSON response to a file
    with open(output_file_path, "w") as output_file:
        json.dump(response_data, output_file, indent=4)  # indent for pretty formatting
    output_list = [output_file_path, file_str]
    return output_list   


default_args ={
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 6, 1),
    'email': ['userEmail@gmail.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 2,
    'retry_delay': timedelta(seconds=15)
}

with DAG(
    'zillow_analyze_dag',
    default_args=default_args,
    schedule_interval = '@daily',
    catchup=False) as dag:
    
    extract_zillow_data_var = PythonOperator(
        task_id= 'tsk_extract_zillow_data_var',
        python_callable=extract_zillow_data,
        op_kwargs={'url': 'https://zillow-com4.p.rapidapi.com/properties/search', 'querystring': {"location":"Toronto, ON","resultsPerPage":"1000","status":"forSale","sort":"relevance","sortType":"asc"}, 'headers': api_host_key, 'date_string':dt_now_string}
        )
    
    
    load_to_s3 = BashOperator(
        task_id= 'task_load_to_s3',
        bash_command = 'aws s3 mv {{ ti.xcom_pull("tsk_extract_zillow_data_var")[0]}} s3://zillowdataproject-bucket/'
    )
    
    file_in_s3 = S3KeySensor(
        task_id='tsk_file_in_s3',
        bucket_key='{{ti.xcom_pull("tsk_extract_zillow_data_var")[1]}}',
        bucket_name=s3_bucket,
        aws_conn_id='aws_s3_conn',
        wildcard_match=False,  # Set this to True if you want to use wildcards in the prefix
        timeout=120,  # Optional: Timeout for the sensor (in seconds)
        poke_interval=5,  # Optional: Time interval between S3 checks (in seconds)
    )
    
    
    
    
    extract_zillow_data_var >> load_to_s3 >> file_in_s3
    
    
