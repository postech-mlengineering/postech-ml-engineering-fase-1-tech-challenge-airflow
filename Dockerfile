#usa a imagem base oficial do Airflow
FROM apache/airflow:3.1.3

#instala as dependências necessárias para a orquestração
RUN pip install --no-cache-dir \
    pandas \
    requests \
    beautifulsoup4 \
    apache-airflow-providers-postgres
