from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser


def generate_ai_analysis(
    api_key,
    latency,
    jitter,
    packet_loss,
    quality_score,
    category,
    use_case
):
    if not api_key:
        return {
            "success": False,
            "message": "Gemini API key is required."
        }

    try:

        llm = ChatGoogleGenerativeAI(
            model="gemini-3.6-flash",
            temperature=0.3,
            google_api_key=api_key
        )

        prompt = ChatPromptTemplate.from_messages([
            (
                "system",
                """
You are an Internet Connection Quality AI Analyst.

Analyze the user's actual network measurements.

You must use:
- latency
- jitter
- packet loss
- fuzzy quality score
- selected use case

Do not invent or change the measurements.

Return exactly these sections:

SUMMARY:
Give a short explanation of the connection.

PERFORMANCE:
Explain latency, jitter, packet loss and fuzzy score.

USE CASE:
Explain whether the connection is suitable for the selected activity.

RECOMMENDATIONS:
Give exactly 3 practical recommendations.
"""
            ),
            (
                "human",
                """
Network Measurements:

Latency: {latency} ms
Jitter: {jitter} ms
Packet Loss: {packet_loss} %
Fuzzy Quality Score: {score}/100
Fuzzy Category: {category}

Selected Use Case:
{use_case}

Analyze this connection.
"""
            )
        ])

        chain = prompt | llm | StrOutputParser()

        response = chain.invoke({
            "latency": latency,
            "jitter": jitter,
            "packet_loss": packet_loss,
            "score": quality_score,
            "category": category,
            "use_case": use_case
        })

        return {
            "success": True,
            "analysis": response
        }

    except Exception as e:

        return {
            "success": False,
            "message": str(e)
        }