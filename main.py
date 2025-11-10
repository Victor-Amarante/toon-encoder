from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Any
from toon_format import encode, estimate_savings, compare_formats
import json
from loguru import logger

app = FastAPI(title="Convert JSON Data to TOON Format")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Data(BaseModel):
    json_data: Any


@app.get("/health")
def health_check():
    return "API is running"


@app.post("/convert")
async def convert_to_toon(data: Data):
    try:
        toon_str = encode(data.json_data)
        logger.debug(f"TOON String: {toon_str}")
        
        savings = estimate_savings(data.json_data)
        logger.debug(f"Savings: {savings}")
        
        comparison = compare_formats(data.json_data)
        logger.debug(f"Comparison: {comparison}")
        
        return {
            "toon_str": toon_str,
            "savings_percent": round(savings.get("savings_percent"), 2),
            "json_tokens": savings.get("json_tokens"),
            "toon_tokens": savings.get("toon_tokens"),
        }
    except json.JSONDecodeError as e:
        raise HTTPException(status_code=400, detail=f"Invalid JSON: {e}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {e}")
