import time

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser


PROVIDER_CONFIG = {
    "Gemini": {
        "model": "gemini-3.8-flash",
        "secret": "GEMINI_API_KEY",
    },
    "OpenAI (ChatGPT API)": {
        "model": "gpt-5.6-luna",
        "secret": "OPENAI_API_KEY",
    },
    "Groq": {
        "model": "openai/gpt-oss-20b",
        "secret": "GROQ_API_KEY",
    },
}


# Gemini fallback models
GEMINI_FALLBACK_MODELS = [
    "gemini-3.8-flash",
    "gemini-3.7-flash",
    "gemini-3.6-flash",
    "gemini-3.5-flash-lite",
]


SYSTEM_PROMPT = """
You are an Internet Connection Quality AI Analyst.

Analyze the user's actual network measurements.

You must use:
- latency
- jitter
- packet loss
- fuzzy quality score
- selected use case

Do not invent, change, or replace the measurements.

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


def build_llm(provider, api_key, model):

    if provider == "Gemini":

        from langchain_google_genai import ChatGoogleGenerativeAI

        return ChatGoogleGenerativeAI(
            model=model,
            google_api_key=api_key,
            temperature=0.3,
        )

    elif provider == "OpenAI (ChatGPT API)":

        from langchain_openai import ChatOpenAI

        return ChatOpenAI(
            model=model,
            api_key=api_key,
            temperature=0.3,
        )

    elif provider == "Groq":

        from langchain_groq import ChatGroq

        return ChatGroq(
            model=model,
            api_key=api_key,
            temperature=0.3,
        )

    raise ValueError(
        f"Unsupported AI provider: {provider}"
    )


def friendly_error(provider, error):

    message = str(error)
    lower = message.lower()

    if (
        "api_key_invalid" in lower
        or "api key not valid" in lower
        or "invalid api key" in lower
        or "incorrect api key" in lower
    ):
        return (
            f"{provider} API key is invalid. "
            "Please enter a valid API key."
        )

    if "401" in lower or "unauthorized" in lower:
        return (
            f"{provider} authentication failed. "
            "Please check your API key."
        )

    if "403" in lower or "forbidden" in lower:
        return (
            f"{provider} API key does not have permission "
            "to use this API/model."
        )

    if (
        "429" in lower
        or "quota" in lower
        or "rate limit" in lower
    ):
        return (
            f"{provider} API quota or rate limit was reached."
        )

    if (
        "503" in lower
        or "unavailable" in lower
        or "high demand" in lower
    ):
        return (
            f"{provider} is temporarily unavailable. "
            "Please try again or use another AI provider."
        )

    if "404" in lower or "not found" in lower:
        return (
            f"The selected {provider} model is unavailable "
            "for this API/account."
        )

    return message


def is_temporary_gemini_error(error):

    message = str(error).lower()

    return (
        "503" in message
        or "unavailable" in message
        or "high demand" in message
        or "temporarily unavailable" in message
    )


def generate_ai_analysis(
    provider,
    api_key,
    latency,
    jitter,
    packet_loss,
    quality_score,
    category,
    use_case,
    model=None,
):

    if provider not in PROVIDER_CONFIG:

        return {
            "success": False,
            "message": f"Unsupported AI provider: {provider}",
            "provider": provider,
        }

    if not api_key or not api_key.strip():

        return {
            "success": False,
            "message": f"{provider} API key is required.",
            "provider": provider,
        }

    api_key = api_key.strip()


    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                SYSTEM_PROMPT,
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
""",
            ),
        ]
    )


    # =====================================================
    # GEMINI WITH AUTOMATIC FALLBACK
    # =====================================================

    if provider == "Gemini":

        requested_model = (
            model
            or PROVIDER_CONFIG["Gemini"]["model"]
        )

        models_to_try = []

        # Requested model first
        models_to_try.append(requested_model)

        # Then fallback models
        for fallback_model in GEMINI_FALLBACK_MODELS:

            if fallback_model not in models_to_try:

                models_to_try.append(
                    fallback_model
                )


        last_error = None


        for current_model in models_to_try:

            for attempt in range(2):

                try:

                    llm = build_llm(
                        provider,
                        api_key,
                        current_model,
                    )

                    chain = (
                        prompt
                        | llm
                        | StrOutputParser()
                    )

                    response = chain.invoke(
                        {
                            "latency": latency,
                            "jitter": jitter,
                            "packet_loss": packet_loss,
                            "score": quality_score,
                            "category": category,
                            "use_case": use_case,
                        }
                    )

                    return {
                        "success": True,
                        "analysis": response,
                        "provider": provider,
                        "model": current_model,
                    }


                except Exception as error:

                    last_error = error

                    # Retry temporary 503 errors
                    if is_temporary_gemini_error(error):

                        if attempt == 0:

                            time.sleep(2)

                            continue

                        # Move to next Gemini model
                        break

                    # Non-temporary error:
                    # stop immediately
                    return {
                        "success": False,
                        "message": friendly_error(
                            provider,
                            error,
                        ),
                        "provider": provider,
                        "model": current_model,
                    }


        return {
            "success": False,
            "message": (
                "Gemini models are temporarily unavailable. "
                "Tried multiple Gemini models. "
                "Please try again or select another provider."
            ),
            "provider": provider,
            "model": requested_model,
            "details": str(last_error) if last_error else "",
        }


    # =====================================================
    # OPENAI / GROQ
    # =====================================================

    selected_model = (
        model
        or PROVIDER_CONFIG[provider]["model"]
    )

    try:

        llm = build_llm(
            provider,
            api_key,
            selected_model,
        )

        chain = (
            prompt
            | llm
            | StrOutputParser()
        )

        response = chain.invoke(
            {
                "latency": latency,
                "jitter": jitter,
                "packet_loss": packet_loss,
                "score": quality_score,
                "category": category,
                "use_case": use_case,
            }
        )

        return {
            "success": True,
            "analysis": response,
            "provider": provider,
            "model": selected_model,
        }


    except Exception as error:

        return {
            "success": False,
            "message": friendly_error(
                provider,
                error,
            ),
            "provider": provider,
            "model": selected_model,
        }