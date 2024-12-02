import es_connect
from fastapi import APIRouter, HTTPException

router = APIRouter(tags=["Get pages"])

@router.get("/get/new")                 # Виводить 10 найновіших CVE
def GetNew():
    try:
        def GetTenNewVulnerabilities():
            client, INDEX_NAME = es_connect.ElasticConnect()

            filtredVulns = []

            searchQuery = {
                "query": {
                    "match_all": {}
                },
                "sort": [
                    {"dateAdded": "desc"}
                ],
                "size": 10
            }

            response = client.search(index=INDEX_NAME, body=searchQuery)

            filtredVulns = [hit["_source"] for hit in response["hits"]["hits"]]

            return filtredVulns
            
        result = GetTenNewVulnerabilities()
        if not result:
            raise HTTPException(status_code=404, detail="No vulnerabilities found")
        return {"10 newest vulnerabilities": result}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {e}")
