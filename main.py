from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Any
from toon_format import encode, estimate_savings, compare_formats
import json

app = FastAPI(title="Convert JSON Data to TOON Format")


class Data(BaseModel):
    json_data: Any


@app.get("/health")
def health_check():
    return "API is running"


@app.post("/convert")
async def convert_to_toon(data: Data):
    try:
        toon_str = encode(data.json_data)
        savings = estimate_savings(data.json_data)
        comparison = compare_formats(data.json_data)
        return {
            "toon_str": toon_str,
            "savings_result": round(savings.get("savings_percent"), 2),
            "compare_result": comparison,
        }
    except json.JSONDecodeError as e:
        raise HTTPException(status_code=400, detail=f"Invalid JSON: {e}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {e}")
