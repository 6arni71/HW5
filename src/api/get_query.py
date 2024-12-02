import es_connect
from fastapi import APIRouter, HTTPException, Query

router = APIRouter(tags=["Get pages"])

@router.get("/get")                     # Виводить CVE які містять ключове слово
def GetQuery(query: str = Query(..., min_length=1)):
    try:
        def GetVulnsByKeywords():
            client, INDEX_NAME = es_connect.ElasticConnect()            

            filtredVulns = []

            searchQuery = {
                "query": {
                    "query_string": {
                        "query": query 
                    }
                },
            }

            response = client.search(index=INDEX_NAME, body=searchQuery)

            filtredVulns = [hit["_source"] for hit in response["hits"]["hits"]]

            return filtredVulns
        
        result = GetVulnsByKeywords()

        if not result:
            raise HTTPException(status_code=404, detail=f"No vulnerabilities found containing the keyword '{query}'")
        return {"Vulnerabilities found on query": result}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {e}")
