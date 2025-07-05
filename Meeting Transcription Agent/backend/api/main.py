import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from llama_cpp import Llama

# ── CONFIG ─────────────────────────────────────────────────────────────────────
MODEL_PATH = os.path.join(
    os.path.dirname(__file__),
    os.pardir, "models", "llama-2-13b-chat-32k.gguf"
)
if not os.path.isfile(MODEL_PATH):
    raise RuntimeError(f"Model not found at {MODEL_PATH!r}")

# ── SCHEMAS ────────────────────────────────────────────────────────────────────
class Transcript(BaseModel):
    text: str

class SummaryOutput(BaseModel):
    summary: str
    action_items: list[str]

# ── APP INIT ───────────────────────────────────────────────────────────────────
app = FastAPI(title="SummarizeBot Phase 1")

@app.on_event("startup")
def load_llm():
    global llm
    llm = Llama(model_path=MODEL_PATH, n_threads=4)

def run_llm(prompt: str, max_tokens: int = 256) -> str:
    resp = llm(prompt=prompt, max_tokens=max_tokens)
    return resp.choices[0].text.strip()

# ── HEALTHCHECK ───────────────────────────────────────────────────────────────
@app.get("/")
def health_check():
    return {"status": "OK"}

# ── NLP ENDPOINT ──────────────────────────────────────────────────────────────
@app.post("/api/summarize", response_model=SummaryOutput)
def summarize(transcript: Transcript):
    text = transcript.text.strip()
    if not text:
        raise HTTPException(400, "Transcript text is empty.")

    # 1) Summarize
    summary = run_llm(
        "Summarize this meeting transcript in 2–3 sentences:\n\n" + text,
        max_tokens=150
    )

    # 2) Extract action items
    raw = run_llm(
        "Extract action items from this transcript. "
        "One line each as `Task — Owner — Deadline`:\n\n" + text,
        max_tokens=150
    )
    items = [ln.strip() for ln in raw.splitlines() if ln.strip()]

    return SummaryOutput(summary=summary, action_items=items)

# ── ENTRYPOINT ────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
