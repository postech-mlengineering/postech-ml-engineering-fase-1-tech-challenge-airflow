# Repositório do Airflow para o Tech Challenge da Fase 1 da Pós-Graduação em Machine Learning Engineering da FIAP

Este repositório consiste na camada de orquestração desenvolvida com Apache Airflow, responsável por automatizar os fluxos de web scraping e pipeline para atualização dos artefatos do motor de recomendação da API BooksToScrape.

### Arquitetura

O diagrama abaixo ilustra a arquitetura do projeto na sua integridade e com suas principais funcionalidades:

<br><p align='center'><img src='https://github.com/postech-mlengineering/postech-ml-engineering-fase-1-tech-challenge-api/blob/9cc654c78d0fbc3a3b8c7f85d4841364127b5cdd/docs/arquitetura.svg' alt='Arquitetura'></p>

### Pré-requisitos

Certifique-se de ter o Python 3.11, o Poetry 2.1.1 e o Docker 29.1.1 instalados em seu sistema.

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

1. Configure as variáveis de ambiente criando um arquivo .env na raiz do projeto e preencha conforme o conteúdo abaixo:

```bash
#variáveis de sistema para permissões
AIRFLOW_UID=1000
AIRFLOW_GID=0
#configurações de acesso à interface web
_AIRFLOW_WWW_USER_USERNAME=<usuario_de_sua_escolha>
_AIRFLOW_WWW_USER_PASSWORD=<senha_de_sua_escolha>
```

2. Crie a rede externa (necessária para a comunicação entre os serviços):

```bash
docker network create postech_mlengineering_api
```

3. Inicie a aplicação:

```bash
docker-compose up --build
```

A UI do Apache Airflow estará rodando em http://localhost:8080.

Certifique-se de configurar as variáveis de ambiente necessárias para a execução da da rotina na seção Admin -> Variables da UI. 

```bash
API_URL=http://postech_mlengineering_api:5000
API_USERNAME=<usuario_airflow_cadastrado_na_api>
API_PASSWORD=<senha_do_usuario_airflow_cadastrado_na_api>
```

### Tecnologias

| Componente | Tecnologia | Versão | Descrição |
| :--- | :--- | :--- | :--- |
| **Orquestrador** | **Apache Airflow** | `^2.10.0` | Framework para orquestração de workflows |
| **Linguagem** | **Python** | `>=3.11, <3.14` | Linguagem para desenvolvimento de scripts |
| **Infraestrutura** | **Docker** | `29.1.1` | Ferramenta de containerização para paridade entre ambientes |
| **Gerenciamento** | **Poetry** | `2.2.1` | Gerenciador de ambientes virtuais para isolamento de dependências |

### Integrações

O airflow interage com uma API RESTful desenvolvida com Flask que gerencia o banco de dados e um motor de recomendação, disponibilizando os dados para um aplicação web desenvolvida com Streamlit.

Link para o repositório da API: https://github.com/postech-mlengineering/postech-ml-techchallenge-fase-1-api

Link para o repositório do aplicativo web: https://github.com/postech-mlengineering/postech-ml-engineering-fase-1-tech-challenge-web-app

### Deploy

A arquitetura e o deploy foram concebidos para suportar um ecossistema distribuído, utilizando uma instância EC2 na AWS como infraestrutura e Docker para a padronização e o isolamento dos ambientes.

A solução é composta por três camadas de containers integrados:

- **Orquestração (Apache Airflow)**: implementada em containers dedicados, esta camada é responsável pelo agendamento e execução dos pipelines de dados, acionando as rotas de /scrape e /training-data da API

- **API (Flask)**: é o coração da arquitetura. Esta camada interage com o site Books To Scrape para aquisição de dados via web scraping e expõe endpoints para consumo

- **Consumo (Web App Streamlit)**: é a interface web que consome os serviços da API, permitindo que os usuários finais interajam com a API

A comunicação entre os containers é otimizada via Docker network, permitindo a interação entre serviços através de nomes de host em vez de IPs dinâmicos. Essa configuração reduz a latência, elimina custos de tráfego externo e melhora a eficiência ao processar as requisições localmente no host.

Os seviços podem ser acessados nos endereços abaixo:

- **API**: http://18.208.50.37:5000
- **Web App Streamlit**: http://18.208.50.37:8501
- **Apache Airflow**: http://18.208.50.37:8080

#### Persistência

A camada de persistência foi definida em um banco de dados gerenciado via Supabase (integrado à plataforma Vercel). Esta infraestrutura é responsável pela centralização do acervo de livros, pelo histórico de preferências de usuários e pela persistência dos logs de auditoria.

### Link da Apresentação

https://youtu.be/mSAH299OHDs

### Colaboradores

[Jorge Platero](https://github.com/jorgeplatero)

[Leandro Delisposti](https://github.com/LeandroDelisposti)

[Hugo Rodrigues](https://github.com/Nokard)
