import es_connect
from fastapi import APIRouter, HTTPException

router = APIRouter(tags=["Get pages"])

@router.get("/get/known")           # Виводить 10 CVE які були використані в атаках
def GetKnown():
    try:
        def GetKnownRansomwareUse():
            client, INDEX_NAME = es_connect.ElasticConnect()

            filtredVulns = []

            searchQuery = {
                "query": {
                    "match": {  
                        "knownRansomwareCampaignUse": "Known"
                    }
                },         
            "size": 10
            }

            response = client.search(index=INDEX_NAME, body=searchQuery)

            filtredVulns = [hit["_source"] for hit in response["hits"]["hits"]]

            return filtredVulns

        result = GetKnownRansomwareUse()

        if not result:
            raise HTTPException(status_code=404, detail="No vulnerabilities found related to ransomware campaigns")
        return {"Ransomware campaigns were used ": result}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {e}")

