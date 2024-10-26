# provider-sentiment

## Overview

Sentiment analysis project to analyze user reviews of mobile applications used for cellular operators, that is MyTelkomsel, MyXL, MyIM3, and MySF (Smartfren), by scraping data from the Google Play Store. The focus is on performing sentiment analysis using natural language processing (NLP) techniques to understand user satisfaction and identify common issues.

## Tech stacks

| Framework/Technologies       | Roles                                                                         |
| ---------------------------- | ----------------------------------------------------------------------------- |
| Kedro                        | Structuring data engineering and data science pipelines                       |
| PostgreSQL                   | Serves as a data lake for raw data and a data warehouse for preprocessed data |
| Docker                       | Containerize the entire project                                               |
| Apache Airflow (In-progress) | Schedule workflows as DAGs                                                    |
| Tableau                      | Creating visual dashboards and reports                                        |

<!-- ## Rules and guidelines

In order to get the best out of the template:

* Don't remove any lines from the `.gitignore` file we provide
* Make sure your results can be reproduced by following a [data engineering convention](https://docs.kedro.org/en/stable/faq/faq.html#what-is-data-engineering-convention)
* Don't commit data to your repository
* Don't commit any credentials or your local configuration to your repository. Keep all your credentials and local configuration in `conf/local/` -->

## How to install dependencies

Declare any dependencies in `requirements.txt` for `pip` installation.

To install them, run:

```
pip install -r requirements.txt
```

## How to run ETL pipeline using Docker

1. Change directory to root project

   ```
   cd sentiment-provider-app
   ```

2. Run docker-compose:

   ```
   docker-compose up -d
   ```

   -d = Detached mode: Run containers in the background

3. Stop service from running to exit

   ```
   docker-compose down -v
   ```

   -v = Remove named volumes declared in the "volumes" section of the Compose file and anonymous volumes attached to containers

## ETL Pipelines

![etl_pipeline](https://github.com/anggapark/sentiment-provider-app/blob/main/asset/etl_pipeline.png?raw=true)
