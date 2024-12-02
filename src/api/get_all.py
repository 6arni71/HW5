import datetime
import es_connect
from fastapi import APIRouter, HTTPException, Query

router = APIRouter(tags=["Get pages"])

@router.get("/get/all")             # Виводить CVE за останні n днів. Максимум 40 CVE
def GetAll(daysCount: int = Query(5, ge=1, le=365)):
    try:
        def GetAllCveLastFiveDays():
            client, INDEX_NAME = es_connect.ElasticConnect()

            dateFiveDaysAgo = datetime.date.today() - datetime.timedelta(days=daysCount)

            filtredVulns = []

            searchQuery = {
                "query": {
                   "range": {
                            "dateAdded": {
                            "gte": dateFiveDaysAgo 
                        }
                    }
                },
            "sort": [{"dateAdded": "desc"}],               
            "size": 40  
            }

            response = client.search(index=INDEX_NAME, body=searchQuery)

            filtredVulns = [hit["_source"] for hit in response["hits"]["hits"]]

            return filtredVulns
        
        result = GetAllCveLastFiveDays()

        if not result:
            raise HTTPException(status_code=404, detail=f"No vulnerabilities found for the last {daysCount} days")
        return {f"Vulnerabilities for the last {daysCount} days": result}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {e}")
