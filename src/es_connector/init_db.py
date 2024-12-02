import es_connect
from elasticsearch import exceptions
from fastapi import APIRouter, HTTPException
import json

router = APIRouter(tags=["Init-db page"])

@router.get("/init-db")
def LoadDataToDB():
    try:
        def LoadCvesFromFileToDB():
            FILE = "./src/es_connector/known_exploited_vulnerabilities.json"
            client, INDEX_NAME = es_connect.ElasticConnect()

            try:
                if not client.indices.exists(index=INDEX_NAME):
                    client.indices.create(index=INDEX_NAME)
            except exceptions.RequestError as e:    
                raise HTTPException(status_code=500, detail=f"Error creating index: {e}")

            try:
                with open(FILE, "r", encoding="utf-8") as f:
                    cveList = json.loads(f.read())
            except FileNotFoundError as e:
                raise HTTPException(status_code=404, detail=f"File not found") 

            vulnsFromCveList = cveList['vulnerabilities']
                
            try:
                if client.count(index=INDEX_NAME)["count"] != len(vulnsFromCveList):
                    query = {"query": {"match_all": {}}}
                    client.delete_by_query(index=INDEX_NAME, body=query)
                    for i, vuln in enumerate(vulnsFromCveList, start=1):
                        client.index(index=INDEX_NAME, id=f"cve-{i}", document=vuln)
                    return f"All CVEs from {FILE} were successfully updated"
                else:
                    return "There was no need to update the database"
            except exceptions.ElasticsearchException as e:
                raise HTTPException(status_code=500, detail=f"Error updating databases: {e}")

        result = LoadCvesFromFileToDB()

        return {"info": result}     
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {e}")