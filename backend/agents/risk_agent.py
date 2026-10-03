from backend.gemini_client import generate_json_response


def normalize_confidence(value):
    """
    Convert confidence values into percentage form.

    Examples:
    0.98 -> 98
    0.70 -> 70
    98 -> 98
    70 -> 70
    """

    try:
        value = float(value)

        if 0 <= value <= 1:
            return int(round(value * 100))

        return int(round(value))

    except (TypeError, ValueError):
        return 0


def local_risk_assessment(
    message,
    message_analysis,
    scam_analysis,
    url_analysis=None
):

    score = 0
    reasons = []

    text = message.lower()

    # =================================================
    # MESSAGE ANALYSIS
    # =================================================

    if message_analysis.get("suspicious"):

        confidence = normalize_confidence(
            message_analysis.get(
                "confidence",
                0
            )
        )

        score += min(
            30,
            int(confidence * 0.30)
        )

        reasons.extend(
            message_analysis.get(
                "indicators",
                []
            )[:4]
        )

    # =================================================
    # SCAM TYPE
    # =================================================

    scam_type = scam_analysis.get(
        "scam_type",
        "Harmless/Unknown"
    )

    scam_confidence = normalize_confidence(
        scam_analysis.get(
            "confidence",
            0
        )
    )

    high_risk_scams = [
        "Banking Scam",
        "Payment Scam",
        "Investment Scam",
        "Job Scam",
        "Account Takeover",
        "Phishing",
        "Impersonation"
    ]

    medium_risk_scams = [
        "Delivery Scam",
        "Lottery/Prize Scam",
        "Social Engineering"
    ]

    if scam_type in high_risk_scams:

        score += 35

        reasons.append(
            f"Detected scam category: {scam_type}."
        )

    elif scam_type in medium_risk_scams:

        score += 25

        reasons.append(
            f"Detected suspicious pattern: {scam_type}."
        )

    # =================================================
    # SCAM CONFIDENCE
    # =================================================

    if scam_confidence >= 90:

        score += 15

    elif scam_confidence >= 75:

        score += 10

    elif scam_confidence >= 60:

        score += 5

    # =================================================
    # MONEY / PAYMENT
    # =================================================

    payment_words = [
        "pay",
        "payment",
        "processing fee",
        "registration fee",
        "upfront fee",
        "advance fee",
        "transfer money",
        "transfer the amount",
        "transfer funds",
        "send money",
        "send funds",
        "deposit",
        "investment",
        "₹",
        "rs.",
        "rupees"
    ]

    if any(
        word in text
        for word in payment_words
    ):

        score += 15

        reasons.append(
            "The message requests or encourages a financial payment or money transfer."
        )

    # =================================================
    # URGENCY
    # =================================================

    urgency_words = [
        "urgent",
        "immediately",
        "within 24 hours",
        "within 2 hours",
        "within 7 days",
        "last chance",
        "limited time",
        "limited-time",
        "offer expires",
        "expires today",
        "act now",
        "today",
        "quickly"
    ]

    if any(
        word in text
        for word in urgency_words
    ):

        score += 10

        reasons.append(
            "The message uses urgency or an artificial deadline to pressure the recipient."
        )

    # =================================================
    # INVESTMENT SCAM SPECIFIC LOGIC
    # =================================================

    if scam_type == "Investment Scam":

        investment_indicators = 0

        guaranteed_return_words = [
            "guaranteed return",
            "guaranteed returns",
            "guaranteed profit",
            "guaranteed earnings"
        ]

        unrealistic_return_words = [
            "5x",
            "500%",
            "multiply your money",
            "huge returns",
            "high returns",
            "unrealistic returns",
            "₹50,000",
            "50,000"
        ]

        scarcity_words = [
            "limited-time",
            "limited time",
            "few slots",
            "only a few",
            "exclusive opportunity",
            "exclusive"
        ]

        transfer_words = [
            "transfer the amount",
            "transfer funds",
            "transfer money",
            "send money",
            "send funds",
            "invest just"
        ]

        if any(
            word in text
            for word in guaranteed_return_words
        ):

            investment_indicators += 1

            reasons.append(
                "The message promises guaranteed investment returns."
            )

        if any(
            word in text
            for word in unrealistic_return_words
        ):

            investment_indicators += 1

            reasons.append(
                "The message promises unusually high returns within a very short period."
            )

        if any(
            word in text
            for word in scarcity_words
        ):

            investment_indicators += 1

            reasons.append(
                "The investment offer uses artificial scarcity or exclusivity."
            )

        if any(
            word in text
            for word in transfer_words
        ):

            investment_indicators += 1

            reasons.append(
                "The message pressures the recipient to transfer or invest money immediately."
            )

        # Strong investment scam pattern
        if investment_indicators >= 3:

            score += 20

    # =================================================
    # JOB SCAM SPECIFIC LOGIC
    # =================================================

    job_words = [
        "job offer",
        "work from home",
        "work-from-home",
        "salary",
        "hiring",
        "employment"
    ]

    job_fee_words = [
        "processing fee",
        "registration fee",
        "upfront fee",
        "advance fee"
    ]

    if (
        any(word in text for word in job_words)
        and
        any(word in text for word in job_fee_words)
    ):

        score += 20

        reasons.append(
            "The employment offer requests an upfront fee, which is a strong employment-scam indicator."
        )

    # =================================================
    # BANKING / CREDENTIAL PROTECTION
    # =================================================

    banking_words = [
        "bank account",
        "banking",
        "kyc",
        "account will be suspended",
        "account blocked",
        "atm pin",
        "pin",
        "otp",
        "cvv"
    ]

    if (
        scam_type == "Banking Scam"
        and
        any(word in text for word in banking_words)
    ):

        score += 10

        reasons.append(
            "The message requests or threatens access to sensitive banking credentials."
        )

    # =================================================
    # URL ANALYSIS
    # =================================================

    if isinstance(url_analysis, dict):

        highest_score = int(
            url_analysis.get(
                "highest_score",
                0
            )
        )

        highest_risk = url_analysis.get(
            "highest_risk",
            "MINIMAL"
        )

        if highest_score > 0:

            score += min(
                30,
                int(highest_score * 0.30)
            )

            reasons.append(
                f"URL investigation detected {highest_risk} risk."
            )

    # =================================================
    # CAP SCORE
    # =================================================

    score = min(
        100,
        score
    )

    # =================================================
    # RISK LEVEL
    # =================================================

    if score >= 80:

        risk_level = "CRITICAL"

    elif score >= 60:

        risk_level = "HIGH"

    elif score >= 35:

        risk_level = "MEDIUM"

    elif score >= 15:

        risk_level = "LOW"

    else:

        risk_level = "MINIMAL"

    # =================================================
    # IMMEDIATE CAUTION
    # =================================================

    if risk_level == "CRITICAL":

        caution = (
            "Do not interact with the sender, click links, "
            "share credentials, or transfer money."
        )

    elif risk_level == "HIGH":

        caution = (
            "Do not make payments or share sensitive information. "
            "Verify the message through an independent official source."
        )

    elif risk_level == "MEDIUM":

        caution = (
            "Exercise caution and independently verify the sender "
            "before taking any action."
        )

    else:

        caution = (
            "No immediate high-risk action was identified, "
            "but remain cautious with unexpected messages."
        )

    return {
        "risk_level": risk_level,
        "risk_score": score,
        "reasons": list(dict.fromkeys(reasons)),
        "immediate_caution": caution,
        "status": "fallback",
        "source": "Local Security Analysis",
        "ai_error": True
    }


def assess_risk(
    message,
    message_analysis,
    scam_analysis,
    url_analysis=None
):

    prompt = f"""
You are a cybersecurity risk assessment agent.

Assess the overall risk of this message.

MESSAGE:
{message}

MESSAGE ANALYSIS:
{message_analysis}

SCAM ANALYSIS:
{scam_analysis}

URL ANALYSIS:
{url_analysis}

Return ONLY valid JSON:

{{
    "risk_level": "",
    "risk_score": 0,
    "reasons": [],
    "immediate_caution": ""
}}

Risk levels must be one of:

MINIMAL
LOW
MEDIUM
HIGH
CRITICAL

Consider:

- Scam category
- Scam confidence
- Requests for money
- Requests for credentials
- Urgency
- Suspicious URLs
- Account threats
- Employment fraud
- Investment fraud
- Phishing indicators

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
            "risk_level": data.get(
                "risk_level",
                "UNKNOWN"
            ),
            "risk_score": int(
                data.get(
                    "risk_score",
                    0
                )
            ),
            "reasons": data.get(
                "reasons",
                []
            ),
            "immediate_caution": data.get(
                "immediate_caution",
                ""
            ),
            "status": "completed",
            "source": "Gemini AI",
            "ai_error": False
        }

    return local_risk_assessment(
        message,
        message_analysis,
        scam_analysis,
        url_analysis
    )