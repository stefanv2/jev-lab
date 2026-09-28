from fastapi import FastAPI
import os
import requests

app = FastAPI()

GATEWAY_URL = "https://ai-gateway.vercel.sh/v1/evaluate"


@app.get("/api")
def test_jev():
    api_key = os.environ.get("AI_GATEWAY_API_KEY")

    if not api_key:
        return {
            "status": "error",
            "message": "AI_GATEWAY_API_KEY ontbreekt"
        }

    payload = {
        "model": "typesafe-ai/jev",
        "state": (
            "Oracle database alert: ORA-19809. "
            "Fast Recovery Area is 99 percent full. "
            "The archiver is stuck."
        ),
        "questions": {
            "storage_problem": {
                "type": "boolean",
                "instructions": (
                    "Is this primarily a storage or capacity related problem?"
                )
            }
        }
    }

    response = requests.post(
        GATEWAY_URL,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        },
        json=payload,
        timeout=30
    )

    return {
        "http_status": response.status_code,
        "jev_response": response.json()
    }