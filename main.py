from fastapi import FastAPI
from pydantic import BaseModel
from fuzzywuzzy import fuzz

app = FastAPI()

# Define your keywords to match
TARGET_KEYWORDS = ["Chief of Staff", "Head of Operations", "VP Operations", "Strategy & Ops", "Special Projects"]

# Define the expected request payload using Pydantic
class JobEmail(BaseModel):
    from_: str
    subject: str
    body: str

@app.post("/")
async def parse_job_posting(payload: JobEmail):
    combined_text = f"{payload.subject} {payload.body}"

    # Fuzzy matching
    best_match = None
    highest_score = 0
    for keyword in TARGET_KEYWORDS:
        score = fuzz.partial_ratio(combined_text.lower(), keyword.lower())
        if score > highest_score:
            highest_score = score
            best_match = keyword

    if highest_score >= 70:
        return {
            "company": "Unknown Company",
            "title": best_match,
            "link": "https://example.com/job",
            "score": highest_score
        }
    else:
        return {
            "message": "No strong match found",
            "score": highest_score
        }

# This block is not necessary for Render since Render manages the ASGI server
# But it's harmless to leave in for local testing
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
