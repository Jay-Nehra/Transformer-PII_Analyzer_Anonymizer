from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional

from presidio_helpers import analyze, anonymize

app = FastAPI(title="Athena Anonymization API")

class AnalyzeRequest(BaseModel):
    text: str
    model_family: str
    model_path: str
    entities: Optional[list] = None
    threshold: float = 0.35

class AnonymizeRequest(BaseModel):
    text: str
    model_family: str
    model_path: str
    operator: str
    mask_char: Optional[str] = '*'
    number_of_chars: Optional[int] = 15
    encrypt_key: Optional[str] = None
    entities: Optional[list] = None
    threshold: float = 0.35

@app.post("/analyze")
async def analyze_text(request: AnalyzeRequest):
    try:
        analyze_results = analyze(
            model_family=request.model_family,
            model_path=request.model_path,
            text=request.text,
            entities=request.entities,
            score_threshold=request.threshold
        )
        return analyze_results
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/anonymize")
async def anonymize_text(request: AnonymizeRequest):
    try:
        analyze_results = analyze(
            model_family=request.model_family,
            model_path=request.model_path,
            text=request.text,
            entities=request.entities,
            score_threshold=request.threshold
        )

        anonymize_results = anonymize(
            text=request.text,
            operator=request.operator,
            analyze_results=analyze_results,
            mask_char=request.mask_char,
            number_of_chars=request.number_of_chars,
            encrypt_key=request.encrypt_key
        )
        return {"text": anonymize_results.text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
