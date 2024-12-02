from elasticsearch import Elasticsearch

def ElasticConnect():
    ELASTIC_ENDPOINT = "https://my-deployment-54bf99.es.us-central1.gcp.cloud.es.io"
    ELASCTIC_API_KEY = "SUNVd2lKTUIzTElhVFphUkRrZ1Q6MURVWTVicFRSLUdzbk5mRExxWk1RUQ=="
    INDEX_NAME = "cves_index"

    client = Elasticsearch(
        ELASTIC_ENDPOINT, 
        api_key=ELASCTIC_API_KEY,
        )

    return client, INDEX_NAME
