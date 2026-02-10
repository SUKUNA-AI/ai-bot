from fastapi import FastAPI, HTTPException

import time

started_at = time.time()

app = FastAPI(title='SBER QA RAG Service', version='0.1.0')

@app.get('/health')
def health():
    return{'ok': True}


@app.get('/status')
def status():
    return {
        "uptime_s": round(time.time() - started_at, 2),
        "docs_count": 0,
        "chunks_count": 0,
        "index_version": None,
        "embed_model_name": None,
        "llm_backend": "mock",
    }

@app.get("/ready")
def ready():
    checks = {
        "embedder": False,
        "index": False,
        "llm": True,
    }

    if not (is_ready := all(checks.values())):
        raise HTTPException(status_code=503, detail={
            "ready": False,
            "checks": checks}
        )
    
    return {"ready": True, "checks": checks}