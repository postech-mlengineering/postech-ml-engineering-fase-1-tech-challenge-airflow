import logging
import requests
from datetime import datetime
from airflow import DAG
from airflow.providers.standard.operators.python import PythonOperator
from airflow.models import Variable


def login_to_api(**kwargs):
    api_url = Variable.get('API_URL')
    username = Variable.get('API_USERNAME')
    password = Variable.get('API_PASSWORD')
    
    login_data = {'username': username, 'password': password}
    logging.info(f'Realizando login em: {api_url}/api/v1/auth/login')
    
    try:
        response = requests.post(f'{api_url}/api/v1/auth/login', json=login_data, timeout=30)
        response.raise_for_status()
        
        data = response.json()
        access_token = data.get('access_token')
        user_id = data.get('user_id')
        
        if not access_token:
            raise ValueError('Token não encontrado na resposta da API.')
            
        kwargs['ti'].xcom_push(key='api_access_token', value=access_token)
        logging.info(f'Login bem-sucedido para o user_id: {user_id}')
    except requests.exceptions.RequestException as e:
        logging.error(f'Erro no login: {e.response.json().get("error") if e.response else e}')
        raise


def run_scrape(**kwargs):
    ti = kwargs['ti']
    api_url = Variable.get('API_URL')
    access_token = ti.xcom_pull(task_ids='login', key='api_access_token')
    
    headers = {'Authorization': f'Bearer {access_token}', 'Content-Type': 'application/json'}
    
    logging.info(f'Iniciando Scraping: {api_url}/api/v1/scrape')
    response = requests.post(f'{api_url}/api/v1/scrape', headers=headers, timeout=600)
    response.raise_for_status()
    logging.info('Scraping finalizado com sucesso.')

def run_training_data(**kwargs):
    ti = kwargs['ti']
    api_url = Variable.get('API_URL')
    access_token = ti.xcom_pull(task_ids='login', key='api_access_token')
    
    headers = {'Authorization': f'Bearer {access_token}'}
    logging.info(f'Iniciando Processamento de ML: {api_url}/api/v1/ml/training-data')

    try:
        response = requests.get(f'{api_url}/api/v1/ml/training-data', headers=headers, timeout=1800)
        response.raise_for_status()
        
        result = response.json()
        logging.info(f'{result.get("msg")}. Artefatos: {result.get("artifacts_saved")}')
    except requests.exceptions.RequestException as e:
        logging.error(f'Erro no pipeline de ML: {e.response.json().get("error") if e.response else e}')
        raise


with DAG(
    dag_id='bookstoscrape',
    start_date=datetime(2025, 12, 9),
    schedule='@daily',
    catchup=False,
    tags=['api', 'scraping', 'machine-learning'],
    doc_md='Orquestra o ciclo completo de dados para o motor de recomendação.'
) as dag:
    
    task_login = PythonOperator(task_id='login', python_callable=login_to_api)
    task_scrape = PythonOperator(task_id='run_scrape', python_callable=run_scrape)
    task_training_data = PythonOperator(task_id='run_training_data', python_callable=run_training_data)

    task_login >> task_scrape >> task_training_data