from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from network_test import ping_host
from fuzzy_logic import calculate_quality
from ai_analyzer import generate_ai_analysis


app = FastAPI(
    title="NetSense AI",
    description="AI + Fuzzy Logic Internet Connection Quality Analyzer",
    version="1.0"
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


class AnalyzeRequest(BaseModel):

    api_key: str
    use_case: str = "Gaming"


@app.get("/")
def home():

    return {
        "message": "NetSense AI API is running"
    }


@app.post("/analyze")
def analyze_network(request: AnalyzeRequest):

    # -------------------------
    # NETWORK TEST
    # -------------------------

    network = ping_host()

    latency = network["latency"]
    jitter = network["jitter"]
    packet_loss = network["packet_loss"]


    # -------------------------
    # FUZZY LOGIC
    # -------------------------

    fuzzy = calculate_quality(
        latency,
        jitter,
        packet_loss
    )


    # -------------------------
    # LANGCHAIN + GEMINI
    # -------------------------

    ai = generate_ai_analysis(
        api_key=request.api_key,
        latency=latency,
        jitter=jitter,
        packet_loss=packet_loss,
        quality_score=fuzzy["score"],
        category=fuzzy["category"],
        use_case=request.use_case
    )


    return {

        "success": True,

        "network": {
            "latency": latency,
            "jitter": jitter,
            "packet_loss": packet_loss
        },

        "fuzzy": fuzzy,

        "ai": ai,

        "use_case": request.use_case
    }