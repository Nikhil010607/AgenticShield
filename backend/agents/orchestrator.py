from backend.agents.message_agent import analyze_message
from backend.agents.scam_agent import detect_scam
from backend.agents.risk_agent import assess_risk
from backend.agents.recommendation_agent import generate_recommendations

from backend.tools.url_checker import analyze_message_urls


def investigate_message(message):

    # -----------------------------------------
    # AGENT 1 — MESSAGE ANALYSIS
    # -----------------------------------------

    message_analysis = analyze_message(
        message
    )

    # -----------------------------------------
    # AGENT 2 — URL ANALYSIS
    # -----------------------------------------

    url_analysis = analyze_message_urls(
        message
    )

    # -----------------------------------------
    # AGENT 3 — SCAM CLASSIFICATION
    # -----------------------------------------

    scam_analysis = detect_scam(
        message
    )

    # -----------------------------------------
    # AGENT 4 — RISK ASSESSMENT
    # -----------------------------------------

    risk_analysis = assess_risk(
        message,
        message_analysis,
        scam_analysis,
        url_analysis
    )

    # -----------------------------------------
    # AGENT 5 — RECOMMENDATION
    # -----------------------------------------

    recommendations = generate_recommendations(
        message,
        message_analysis,
        scam_analysis,
        risk_analysis,
        url_analysis
    )

    # -----------------------------------------
    # AGENT STATUS
    # -----------------------------------------

    agents = [

        {
            "name": "Message Analysis Agent",
            "status": message_analysis.get(
                "status",
                "completed"
            ),
            "result": message_analysis
        },

        {
            "name": "URL Investigation Agent",
            "status": url_analysis.get(
                "status",
                "completed"
            ),
            "result": url_analysis
        },

        {
            "name": "Scam Pattern Agent",
            "status": scam_analysis.get(
                "status",
                "completed"
            ),
            "result": scam_analysis
        },

        {
            "name": "Risk Assessment Agent",
            "status": risk_analysis.get(
                "status",
                "completed"
            ),
            "result": risk_analysis
        },

        {
            "name": "Recommendation Agent",
            "status": recommendations.get(
                "status",
                "completed"
            ),
            "result": recommendations
        }
    ]

    # -----------------------------------------
    # FINAL RESULT
    # -----------------------------------------

    return {

        "message_analysis": message_analysis,

        "url_analysis": url_analysis,

        "scam_analysis": scam_analysis,

        "risk_analysis": risk_analysis,

        "recommendations": recommendations,

        "agents": agents
    }