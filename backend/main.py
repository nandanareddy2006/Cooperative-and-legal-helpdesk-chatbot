from fastapi import FastAPI

app = FastAPI(
    title="Sahakaar Saathi",
    description="Cooperative Governance & Legal Helpdesk",
    version="0.1.0"
)

@app.get("/")
def root():
    return {
        "project": "Sahakaar Saathi",
        "status": "running",
        "message": "Cooperative Governance & Legal Helpdesk API"
    }

@app.get("/health")
def health():
    return {"status": "healthy"}
