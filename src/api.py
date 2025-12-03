from typing import List, Optional

from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field
import logging

from .capstone.demo import analyze_case



# --- Logging setup ---
logging.basicConfig(level=logging.INFO)


# --- FastAPI app ---
app = FastAPI(
    title="LexFabric Reasoning Engine",
    description="Multi-agent microservice for evidence analysis and timeline reconstruction.",
    version="1.0.0",
)


# --- Pydantic models (data contracts) ---

class AnalysisRequest(BaseModel):
    case_id: str = Field(..., description="Synthetic case ID (e.g., CC02, RH10)")
    query: Optional[str] = Field(
        None,
        description="Optional natural language question to pass into the Q&A stage."
    )


class TimelineEvent(BaseModel):
    date: str
    event: str


class AnalysisResponse(BaseModel):
    case_id: str
    status: str
    steps: List[str]
    timeline: List[TimelineEvent]
    final_answer: Optional[str] = None


# --- Endpoints ---

@app.get("/")
async def root():
    return {
        "service": "LexFabric Reasoning Engine",
        "docs": "/docs",
        "health": "/health"
    }


@app.get("/health", status_code=200)
async def health_check():
    """Simple liveness probe."""
    return {"status": "operational", "service": "LexFabric"}


@app.post("/v1/agent/analyze", response_model=AnalysisResponse, status_code=200)
async def run_analysis(payload: AnalysisRequest):
    """
    Triggers the LexFabric multi-agent (or fallback) analysis pipeline:

    1. Locates synthetic evidence for {case_id}
    2. Reconstructs a deterministic timeline
    3. Optionally processes {query} to compute an answer
    """
    try:
        logging.info(f"[API] Analysis request received for case_id={payload.case_id}")

        result_data = analyze_case(payload.case_id, payload.query)

        return result_data

    except FileNotFoundError as e:
        logging.warning(f"[API] Case not found: {e}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )
    except Exception as e:
        logging.error(f"[API] Internal pipeline error: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal pipeline error. See server logs for details.",
        )
