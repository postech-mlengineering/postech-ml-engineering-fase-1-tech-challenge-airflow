# Repositório do Airflow para o Tech Challenge da Fase 1 da Pós-Graduação em Machine Learning Engineering da FIAP

Este repositório consiste na camada de orquestração desenvolvida com Apache Airflow, projetada para automatizar o ciclo de vida dos dados ao integrar o fluxo de extração (web scraping) à atualização periódica das matrizes de similaridade baseadas em TF-IDF. Por meio da coordenação do workflow de ETL e da sincronização dos artefatos de ML, a solução estabelece uma arquitetura ML-ready que assegura a integridade e a disponibilidade de informações atualizadas para consumo.

### Arquitetura

O diagrama abaixo ilustra a arquitetura do projeto na sua integridade e com suas principais funcionalidades:

<br><p align='center'><img src='https://github.com/postech-mlengineering/postech-ml-engineering-fase-1-tech-challenge-api/blob/9cc654c78d0fbc3a3b8c7f85d4841364127b5cdd/docs/arquitetura.svg' alt='Arquitetura'></p>

### Pré-requisitos

Certifique-se de ter o Python 3.11+ e o Poetry instalados em seu sistema.

Para instalar o Poetry, use o método oficial:

```bash
curl -sSL [https://install.python-poetry.org](https://install.python-poetry.org) | python3 -
```

### Instalação

Clone o repositório e instale as dependências:

```bash
git clone [https://github.com/jorgeplatero/postech-ml-techchallenge-fase-1-airflow.git](https://github.com/jorgeplatero/postech-ml-techchallenge-fase-1-airflow.git)

cd postech-ml-techchallenge-fase-1-airflow

poetry install
```

O Poetry criará um ambiente virtual isolado e instalará todas as bibliotecas necessárias para a execução dos scripts.

### Como Rodar a Aplicação

Para subir o ambiente completo do Airflow (Webserver, Scheduler, Postgres) via Docker:

```bash
docker-compose up -d
```

A API estará rodando em http://localhost:8080. Certifique-se de configurar as variáveis de ambiente necessárias na seção Admin -> Variables da UI.

### Tecnologias

| Componente | Tecnologia | Versão | Descrição |
| :--- | :--- | :--- | :--- |
| **Orquestrador** | **Apache Airflow** | `^2.10.0` | Framework para orquestração de workflows |
| **Linguagem** | **Python** | `>=3.11, <3.14` | Linguagem para desenvolvimento de scripts |
| **Infraestrutura** | **Docker** | `3.8 (Compose)` | Ferramenta de containerização para paridade entre ambientes |
| **Gerenciamento** | **Poetry** | `2.2.1` | Gerenciador de ambientes virtuais para isolamento de dependências |

### Integrações

O airflow interage com uma API RESTful desenvolvida com Flask que gerencia o banco de dados e um motor de recomendação, disponibilizando os dados para um aplicação web desenvolvida com Streamlit.

Link para o repositório da API: https://github.com/postech-mlengineering/postech-ml-techchallenge-fase-1-api

Link para o repositório do aplicativo web: https://github.com/postech-mlengineering/postech-ml-engineering-fase-1-tech-challenge-web-app

### Deploy

A arquitetura e o deploy foram concebidos para suportar um ecossistema distribuído, utilizando a AWS (EC2) como provedor de infraestrutura e Docker para a padronização e o isolamento dos ambientes de execução.

A solução é composta por três camadas principais de containers integrados:

* **Orquestração (Apache Airflow)**: implementada em containers dedicados, esta camada é responsável pelo agendamento e execução dos pipelines de dados, acionando as rotas de /scrape e /training-data da API

* **API (Flask)**: é o coração da arquitetura, onde a lógica de negócio e o motor de recomendações reside. Esta camada interage com o site Books To Scrape para aquisição de dados via web scraping e expõe endpoints para consumo

* **Consumo (Streamlit)**: é a interface web que consome os serviços da API, permitindo que os usuários finais interajam com a API

A comunicação entre os containers é otimizada por meio da atribuição de rede comum no Docker, permitindo que os serviços interajam através de nomes de host predefinidos em vez de IPs dinâmicos, elevando a eficiência e performance ao processar o tráfego de dados localmente na interface do host, o que reduz a latência e elimina custos de saída.

#### Persistência

A camada de persistência é estruturada por meio de um banco de dados relacional gerenciado via Supabase (integrado à plataforma Vercel). Esta infraestrutura é responsável pela centralização do acervo de livros, pelo histórico de preferências de usuários e pela persistência dos logs de auditoria.
