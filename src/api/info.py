from fastapi import APIRouter, HTTPException

router = APIRouter(tags=["Info page"])

@router.get("/info")
def GetInfo():
    try:
        aboutApp = (
            "Програма для отримання інформації про CVE з БД Elasticsearch."
            " За допомогою даної програми можна:"
            " 1. Отримати додані CVE протягом n днів."
            " 2. Отримати дані про 10 найновіших CVE."
            " 3. Отримати 10 вразливостей, які були використані в атаках."
            " 4. Пошук CVE за ключовим словом."
        )
        aboutCreator = "Габрильчук Андрій Васильович"
        return {
            "app": aboutApp,
            "creator": aboutCreator
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {e}")
 
# #інфа про мене і програму


