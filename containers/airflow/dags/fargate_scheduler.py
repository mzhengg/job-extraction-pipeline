from airflow import DAG
from airflow.providers.amazon.aws.operators.ecs import EcsRegisterTaskDefinitionOperator, EcsDeregisterTaskDefinitionOperator

default_args = {
    'owner': 'airflow',
    'start_date': '2022-1-1',
    'depends_on_past': False, # determines if task should be triggered if previous task hasn't succeeded
    'retries': 1 # number of retries that should be performed before failing the task
}

with DAG(
    dag_id = 'fargate_scheduler_dag',
    schedule_interval = '@weekly',
    default_args = default_args,
    catchup = False, # determines if DAG should run for any data interval not run since the last interval
    max_active_runs = 1, # total number of tasks that can run at the same time for a given DAG run
    tags = ['fargate-dag'],

) as dag:
    register_task_definition = EcsRegisterTaskDefinitionOperator(
        task_id = 'register_task_definition', # airflow task id
        family = 'indeed-scraper-ecs-task', # task definition name
        container_definition = [ # container definition
            {
                'name': 'indeed-scraper-etl-container',
                'image': '316226119737.dkr.ecr.us-east-1.amazonaws.com/indeed-scraper-ecs-repository:latest',
                'environmentFiles': [
                    {
                        'value': 'arn:aws:s3:::indeed-scraper-s3-bucket/environment files/.env',
                        'type': 's3'
                    }
                ]
            }
        ],
        register_task_definition = {
            'cpu': '1024', # equivalent to 1 vCPU
            'memory': '3072', # equivalent to 3 GB
            'networkMode': 'awsvpc',
            'compatibilities': ['FARGATE']
        }
    )
