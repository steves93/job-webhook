from fastapi import FastAPI
from pydantic import BaseModel, Field
from fuzzywuzzy import fuzz

app = FastAPI()

TARGET_KEYWORDS = ["Chief of Staff", "Head of Operations", "VP Operations", "Strategy & Ops", "Special Projects"]

class JobEmail(BaseModel):
    from_: str = Field(default="unknown@example.com")
    subject: str = Field(default="No Subject")
    body: str = Field(default="No Body")

@app.post("/")
async def parse_job_posting(payload: JobEmail):
    # Combine subject and body safely
    combined_text = f"{payload.subject or ''} {payload.body or ''}"

    best_match = None
    highest_score = 0
    for keyword in TARGET_KEYWORDS:
        score = fuzz.partial_ratio(combined_text.lower(), keyword.lower())
        if score > highest_score:
            highest_score = score
            best_match = keyword

    # Always return consistent structure, even if score is low
    return {
        "company": "Unknown Company",
        "title": best_match or "Unknown Title",
        "link": "https://example.com/job",
        "score": highest_score
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
