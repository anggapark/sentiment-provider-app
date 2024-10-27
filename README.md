# provider-sentiment

## Overview

Sentiment analysis project to analyze user reviews of mobile applications used for cellular operators, that is MyTelkomsel, MyXL, MyIM3, and MySF (Smartfren), by scraping data from the Google Play Store. The focus is on performing sentiment analysis using natural language processing (NLP) techniques to understand user satisfaction and identify common issues.

## Tech stacks

| Framework/Technologies | Roles                                                                         |
| ---------------------- | ----------------------------------------------------------------------------- |
| Kedro                  | Structuring data engineering and data science pipelines                       |
| PostgreSQL             | Serves as a data lake for raw data and a data warehouse for preprocessed data |
| Docker                 | Containerize the entire project                                               |
| Apache Airflow         | Schedule workflows as DAGs                                                    |
| Tableau                | Creating visual dashboards and reports                                        |

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

## How to run ETL and ML pipeline using Docker

1. Change directory to root project

   ```
   cd sentiment-provider-app
   ```

2. Initialize airflow within docker:

   ```
   docker-compose up init-airflow -d
   ```

   -d = Detached mode: Run containers in the background

3. Run docker-compose:

   ```
   docker-compose up
   ```

4. To open Airflow, visit this link in browser
   ```
   http://localhost:8080/
   ```

How to stop service from running:

```
docker-compose down -v
```

-v = Remove named volumes declared in the "volumes" section of the Compose file and anonymous volumes attached to containers

## How to Access API

1. Change to deploy directory

   ```
   cd deploy
   ```

2. Run the API
   ```
   uvicorn api:app --reload
   ```
3. Test the API
   ```bash
   curl -X 'POST' \
   'http://127.0.0.1:8000/predict' \
   -H 'accept: application/json' \
   -H 'Content-Type: application/json' \
   -d '{
   "text": "aplikasi ini bagus tapi sinyalnya jelek dan kadang lemot"
   }'
   ```
   you should receive JSON respons:
   ```json
   { "Sentiment": "Negative" }
   ```

## ETL Pipelines

![etl_pipeline](https://github.com/anggapark/sentiment-provider-app/blob/main/asset/etl_pipeline.png?raw=true)

The Extract-Transform-Load pipeline are:

1.  Extract
    - Scrape data from google play store
    - Store csv file in device for manual labelling
    - Dump labeled dataset into postgres
2.  Transform

    - Combine datasets
    - Remove missing value
    - Remove review that has only emoji
    - Case folding
    - Add space after punctuations to prevent each word to combined after punctuation removal
      <details>
      <summary>Example</summary>
      <br>

           Input: "Aplikasi yang sangat buruk,jelek,pembohong"
           Output: "Aplikasi yang sangat buruk, jelek, pembohong"

      </details>

    - Remove punctuation characters
    - Remove non-ASCII characters from the input text
    - Removes URLs
    - Stemming (Reduces words to their root form)
    - Replace slang words in the input texts with their formal equivalents using [colloquial-indonesian-lexicon](https://github.com/anggapark/sentiment-provider-app/blob/main/colloquial-indonesian-lexicon-v3.csv) dictionary
    - Remove specific irrelevant words, such as brand name
    - Fix letter repetition
      <details>
      <summary>Example</summary>
      <br>

          "mmantap" -> "mantap",
          "mannntap" -> "mantap",
          "mantapp" -> "mantap"

      </details>

    - Remove reviews with less than 2 words
    - Label encoding
    - Remove empty string after preprocessing

3.  Load
    - Store transformed data in postgres as data warehouse
    - Data in data warehouse can be used for dashboard and machine learning
