from backend.gemini_client import generate_json_response


def local_recommendations(
    message,
    message_analysis,
    scam_analysis,
    risk_analysis,
    url_analysis=None
):
    scam_type = scam_analysis.get(
        "scam_type",
        "Harmless/Unknown"
    )

    risk_level = risk_analysis.get(
        "risk_level",
        "LOW"
    )

    risk_score = int(
        risk_analysis.get(
            "risk_score",
            0
        )
    )

    # =================================================
    # HARMLESS / LOW-RISK MESSAGE
    # =================================================

    if (
        scam_type == "Harmless/Unknown"
        and risk_score < 35
        and risk_level in ["MINIMAL", "LOW"]
    ):
        return {
            "immediate_actions": [
                "No immediate action is required.",
                "The message does not contain strong scam indicators."
            ],
            "avoid": [
                "No specific suspicious behavior was detected.",
                "Continue to exercise normal caution with unexpected requests."
            ],
            "verification": (
                "No additional verification is required based on "
                "the detected content."
            ),
            "reporting_advice": (
                "No scam reporting is necessary unless suspicious "
                "behavior is identified later."
            ),
            "status": "fallback",
            "source": "Local Security Analysis",
            "ai_error": True
        }

    # =================================================
    # HIGH / CRITICAL RISK
    # =================================================

    if risk_level in ["HIGH", "CRITICAL"]:

        immediate_actions = [
            "Do not interact with suspicious links or requests.",
            "Do not provide passwords, PINs, OTPs or other sensitive information.",
            "Verify the sender through an independent official source."
        ]

        avoid = [
            "Do not make payments based only on the message.",
            "Do not share banking, identity or personal information.",
            "Do not allow urgency or pressure to influence your decision."
        ]

        verification = (
            "Independently verify the sender or organization using "
            "its official website, application or verified contact details."
        )

        reporting = (
            "Block and report the sender through the messaging platform. "
            "For suspected financial fraud in India, consider reporting "
            "it through the National Cyber Crime Reporting Portal or "
            "the cybercrime helpline 1930."
        )

        # Job scam
        if scam_type == "Job Scam":

            immediate_actions = [
                "Do not pay the requested processing, registration or security fee.",
                "Stop communication with the sender until the job offer is independently verified.",
                "Save screenshots of the message and sender details."
            ]

            avoid = [
                "Do not pay any upfront employment fee.",
                "Do not share personal, banking or identity documents.",
                "Do not allow artificial deadlines to pressure you into paying."
            ]

            verification = (
                "Independently visit the organization's official careers "
                "website and verify the vacancy or contact its verified "
                "Human Resources department."
            )

        # Banking scam
        elif scam_type == "Banking Scam":

            immediate_actions = [
                "Do not click suspicious banking links.",
                "Do not provide passwords, PINs or OTPs.",
                "Verify the message through the bank's official website or app."
            ]

            avoid = [
                "Do not reply to the sender.",
                "Do not share banking or personal information.",
                "Do not make payments based only on the message."
            ]

            verification = (
                "Contact the bank using an official customer-service number "
                "or access its official application manually."
            )
                    # Investment scam
        elif scam_type == "Investment Scam":

            immediate_actions = [
                "Do not transfer money or invest based on this message.",
                "Do not send funds to the provided bank account, wallet or payment address.",
                "Stop communication until the investment opportunity is independently verified."
            ]

            avoid = [
                "Do not trust guaranteed or unusually high returns.",
                "Do not share banking, identity or financial information.",
                "Do not allow limited-time offers or pressure to influence your decision."
            ]

            verification = (
                "Verify the investment company and opportunity independently "
                "through official regulatory or company sources before making "
                "any financial decision."
            )

        return {
            "immediate_actions": immediate_actions,
            "avoid": avoid,
            "verification": verification,
            "reporting_advice": reporting,
            "status": "fallback",
            "source": "Local Security Analysis",
            "ai_error": True
        }

    # =================================================
    # MEDIUM RISK
    # =================================================

    return {
        "immediate_actions": [
            "Do not take financial or security-sensitive action until the message is verified.",
            "Check the sender and context carefully."
        ],
        "avoid": [
            "Do not share sensitive personal or financial information.",
            "Do not click unexpected links until they are verified."
        ],
        "verification": (
            "Verify the sender independently using an official "
            "website or trusted contact method."
        ),
        "reporting_advice": (
            "If the message is confirmed to be fraudulent, block and "
            "report the sender through the relevant platform."
        ),
        "status": "fallback",
        "source": "Local Security Analysis",
        "ai_error": True
    }


def generate_recommendations(
    message,
    message_analysis,
    scam_analysis,
    risk_analysis,
    url_analysis=None
):

    prompt = f"""
You are a cybersecurity recommendation agent.

Based on the investigation below, provide appropriate safety recommendations.

MESSAGE:
{message}

MESSAGE ANALYSIS:
{message_analysis}

SCAM ANALYSIS:
{scam_analysis}

RISK ANALYSIS:
{risk_analysis}

URL ANALYSIS:
{url_analysis}

Return ONLY valid JSON:

{{
    "immediate_actions": [],
    "avoid": [],
    "verification": "",
    "reporting_advice": ""
}}

IMPORTANT:

If the message is harmless and the risk is MINIMAL or LOW:
- Do NOT give generic scam warnings.
- Say that no immediate action is required.
- Do NOT tell the user to report or block a normal message.

If the message is HIGH or CRITICAL risk:
- Give specific actions based on the detected scam type.
- Mention payment protection for payment/job/investment scams.
- Mention credential protection for phishing/banking scams.
- Give appropriate verification advice.

Do not add markdown.
Do not add explanations outside the JSON.
"""

    result = generate_json_response(prompt)

    if result.get("success"):

        data = result.get(
            "data",
            {}
        )

        return {
            "immediate_actions": data.get(
                "immediate_actions",
                []
            ),
            "avoid": data.get(
                "avoid",
                []
            ),
            "verification": data.get(
                "verification",
                ""
            ),
            "reporting_advice": data.get(
                "reporting_advice",
                ""
            ),
            "status": "completed",
            "source": "Gemini AI",
            "ai_error": False
        }

    return local_recommendations(
        message,
        message_analysis,
        scam_analysis,
        risk_analysis,
        url_analysis
    )