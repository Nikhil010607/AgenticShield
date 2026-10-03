from backend.gemini_client import generate_json_response


def local_scam_detection(message):

    text = message.lower()

    scores = {
        "Banking Scam": 0,
        "Phishing": 0,
        "Payment Scam": 0,
        "Job Scam": 0,
        "Investment Scam": 0,
        "Lottery/Prize Scam": 0,
        "Delivery Scam": 0,
        "Impersonation": 0,
        "Account Takeover": 0,
        "Social Engineering": 0
    }

    # Banking indicators
    banking_terms = [
        "bank",
        "bank account",
        "kyc",
        "atm pin",
        "internet banking",
        "account suspension",
        "account blocked"
    ]

    for term in banking_terms:
        if term in text:
            scores["Banking Scam"] += 10

    # Credential / phishing indicators
    phishing_terms = [
        "password",
        "otp",
        "pin",
        "verify",
        "verification",
        "login",
        "click",
        "http://",
        "https://"
    ]

    for term in phishing_terms:
        if term in text:
            scores["Phishing"] += 8

    # Payment indicators
    payment_terms = [
        "pay",
        "payment",
        "processing fee",
        "transfer money",
        "send money"
    ]

    for term in payment_terms:
        if term in text:
            scores["Payment Scam"] += 10

    # Job scam indicators
    job_terms = [
        "job offer",
        "work from home",
        "salary",
        "hiring",
        "vacancy",
        "recruitment"
    ]

    for term in job_terms:
        if term in text:
            scores["Job Scam"] += 10

    # Investment scam indicators
    investment_terms = [
        "investment",
        "profit",
        "returns",
        "crypto",
        "trading",
        "double your money"
    ]

    for term in investment_terms:
        if term in text:
            scores["Investment Scam"] += 10

    # Lottery / prize indicators
    prize_terms = [
        "won",
        "winner",
        "lottery",
        "prize",
        "lucky draw",
        "reward"
    ]

    for term in prize_terms:
        if term in text:
            scores["Lottery/Prize Scam"] += 10

    # Delivery scam
    delivery_terms = [
        "delivery",
        "parcel",
        "package",
        "courier",
        "shipment"
    ]

    for term in delivery_terms:
        if term in text:
            scores["Delivery Scam"] += 10

    # Impersonation
    impersonation_terms = [
        "dear customer",
        "bank security",
        "official",
        "department",
        "customer support"
    ]

    for term in impersonation_terms:
        if term in text:
            scores["Impersonation"] += 8

    # Account takeover
    takeover_terms = [
        "account blocked",
        "account suspended",
        "verify your account",
        "login",
        "password",
        "otp"
    ]

    for term in takeover_terms:
        if term in text:
            scores["Account Takeover"] += 8

    # Social engineering
    social_terms = [
        "urgent",
        "immediately",
        "within 24 hours",
        "last chance",
        "permanently",
        "suspended",
        "blocked",
        "failure to"
    ]

    for term in social_terms:
        if term in text:
            scores["Social Engineering"] += 8

    # Find strongest category
    scam_type = max(
        scores,
        key=scores.get
    )

    score = scores[scam_type]

    # If almost no indicators exist
    if score < 10:

        return {
            "scam_type": "Harmless/Unknown",
            "confidence": 30,
            "reason": (
                "No strong scam indicators were detected "
                "using the local rule-based analysis."
            )
        }

    confidence = min(
        98,
        50 + score
    )

    # Banking + phishing should be classified as Banking Scam
    if (
        scores["Banking Scam"] >= 20
        and scores["Phishing"] >= 16
    ):

        scam_type = "Banking Scam"

        confidence = min(
            98,
            70 + scores["Banking Scam"] // 2
        )

    return {
        "scam_type": scam_type,
        "confidence": confidence,
        "reason": (
            "Local analysis detected indicators associated with "
            f"{scam_type}."
        )
    }


def detect_scam(message):

    prompt = f"""
You are the Scam Pattern Detection Agent in AgentShield.

Classify the message into the most appropriate scam category.

MESSAGE:
{message}

Allowed categories:

- Phishing
- Banking Scam
- Payment Scam
- Job Scam
- Investment Scam
- Lottery/Prize Scam
- Delivery Scam
- Impersonation
- Account Takeover
- Social Engineering
- Harmless/Unknown

Analyze:

- Message content
- Requested information
- Requested payment
- Urgency
- Threats
- Links
- Impersonation
- Social engineering
- Credential requests

Return ONLY valid JSON:

{{
    "scam_type": "",
    "confidence": 0,
    "reason": ""
}}

Rules:

- scam_type must be one of the allowed categories
- confidence must be between 0 and 100
- reason must explain the classification
- Do not include markdown
- Do not include ```json
"""

    result = generate_json_response(prompt)

    # Gemini successful
    if result.get("success"):

        data = result.get(
            "data",
            {}
        )

        return {
            "scam_type": data.get(
                "scam_type",
                "Harmless/Unknown"
            ),
            "confidence": int(
                data.get(
                    "confidence",
                    0
                )
            ),
            "reason": data.get(
                "reason",
                ""
            ),
            "status": "completed",
            "source": "Gemini AI"
        }

    # Gemini unavailable → local fallback
    fallback = local_scam_detection(
        message
    )

    return {
        "scam_type": fallback["scam_type"],
        "confidence": fallback["confidence"],
        "reason": (
            fallback["reason"]
            + " Gemini AI was temporarily unavailable, "
            "so local security rules were used."
        ),
        "status": "fallback",
        "source": "Local Security Analysis",
        "ai_error": True
    }