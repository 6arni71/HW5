import es_connect

client, INDEX_NAME = es_connect.ElasticConnect()

query = {"query": {"match_all": {}}}
client.delete_by_query(index=INDEX_NAME, body=query)