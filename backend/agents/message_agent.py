import re
from backend.gemini_client import generate_json_response


def local_message_analysis(message):
    """
    Local fallback analysis for suspicious messages.
    Generates indicators based on the actual patterns found in the message.
    """

    text = message.lower()
    indicators = []

    # =========================================================
    # COMMON PATTERNS
    # =========================================================

    urgency_words = [
        "urgent",
        "immediately",
        "within 24 hours",
        "today",
        "limited time",
        "last chance",
        "act now",
        "expire",
        "expires",
        "quickly"
    ]

    banking_words = [
        "bank",
        "bank account",
        "kyc",
        "atm",
        "pin",
        "otp",
        "internet banking",
        "account number",
        "account blocked",
        "account suspended"
    ]

    credential_words = [
        "password",
        "otp",
        "pin",
        "login",
        "username",
        "account number",
        "card number"
    ]

    payment_words = [
        "pay",
        "payment",
        "transfer",
        "send money",
        "processing fee",
        "registration fee",
        "deposit",
        "transaction"
    ]

    url_pattern = r"https?://[^\s]+"

    # =========================================================
    # GENERAL INDICATORS
    # =========================================================

    if any(word in text for word in urgency_words):
        indicators.append(
            "Uses urgent or time-sensitive language to pressure the recipient."
        )

    if any(word in text for word in banking_words):
        indicators.append(
            "Contains banking or financial account-related information."
        )

    if any(word in text for word in credential_words):
        indicators.append(
            "Requests or references sensitive credentials such as OTP, PIN, password, or account details."
        )

    if re.search(url_pattern, text):
        indicators.append(
            "Contains a URL that may require further investigation."
        )

    # =========================================================
    # JOB SCAM
    # =========================================================

    job_words = [
    "job",
    "job offer",
    "work from home",
    "employment",
    "employment offer",
    "hiring",
    "vacancy",
    "recruitment",
    "recruiting",
    "salary",
    "career",
    "career opportunity",
    "job position"
]
    job_fee_words = [
        "processing fee",
        "registration fee",
        "joining fee",
        "training fee",
        "pay to confirm",
        "pay to secure"
    ]

    has_job_context = any(word in text for word in job_words)
    has_job_fee = any(word in text for word in job_fee_words)

    if has_job_context:
        indicators.append(
            "Contains an unsolicited job or employment-related offer."
        )

    if has_job_context and has_job_fee:
        indicators.append(
            "Requests an upfront fee to obtain or confirm the job."
        )

    if has_job_context and any(
        phrase in text
        for phrase in [
            "high salary",
            "huge salary",
            "₹",
            "per month",
            "guaranteed income",
            "easy money"
        ]
    ):
        indicators.append(
            "Uses an attractive financial incentive to make the job offer appear appealing."
        )

    if has_job_context and any(word in text for word in urgency_words):
        indicators.append(
            "Uses urgency to pressure the recipient into accepting the job offer quickly."
        )

    # =========================================================
    # INVESTMENT SCAM
    # =========================================================

    investment_words = [
        "investment",
        "invest",
        "returns",
        "guaranteed returns",
        "profit",
        "trading",
        "crypto",
        "cryptocurrency",
        "double your money",
        "multiply your money"
    ]

    has_investment_context = any(
        word in text for word in investment_words
    )

    if has_investment_context:
        indicators.append(
            "Promotes an investment or financial opportunity."
        )

    if has_investment_context and any(
        phrase in text
        for phrase in [
            "guaranteed return",
            "guaranteed returns",
            "double your money",
            "multiply your money",
            "huge profit",
            "high profit"
        ]
    ):
        indicators.append(
            "Promises unusually high or guaranteed financial returns."
        )

    if has_investment_context and any(word in text for word in urgency_words):
        indicators.append(
            "Creates urgency to encourage immediate investment."
        )

    if has_investment_context and any(
        word in text
        for word in [
            "transfer",
            "send money",
            "deposit",
            "invest today"
        ]
    ):
        indicators.append(
            "Encourages the recipient to transfer or deposit money."
        )

    # =========================================================
    # BANKING / PHISHING
    # =========================================================

    has_banking_context = any(
        word in text for word in banking_words
    )

    if has_banking_context and any(
        word in text
        for word in [
            "suspended",
            "blocked",
            "verify",
            "verification"
        ]
    ):
        indicators.append(
            "Uses account suspension or verification pressure to obtain banking information."
        )

    if has_banking_context and any(
        word in text for word in [
            "otp",
            "pin",
            "password",
            "account number"
        ]
    ):
        indicators.append(
            "Requests sensitive banking credentials or authentication information."
        )

    # =========================================================
    # LOTTERY / PRIZE SCAM
    # =========================================================

    prize_words = [
        "lottery",
        "winner",
        "won",
        "prize",
        "lucky draw",
        "reward",
        "cash prize"
    ]

    has_prize_context = any(
        word in text for word in prize_words
    )

    if has_prize_context:
        indicators.append(
            "Claims that the recipient has won a prize, lottery, or reward."
        )

    if has_prize_context and any(
        word in text
        for word in payment_words
    ):
        indicators.append(
            "Requests payment or money-related action in connection with the prize."
        )

    # =========================================================
    # DELIVERY SCAM
    # =========================================================

    delivery_words = [
        "delivery",
        "parcel",
        "package",
        "courier",
        "shipment",
        "delivery failed"
    ]

    has_delivery_context = any(
        word in text for word in delivery_words
    )

    if has_delivery_context:
        indicators.append(
            "References a delivery, parcel, courier, or shipment."
        )

    if has_delivery_context and any(
        word in text
        for word in payment_words
    ):
        indicators.append(
            "Requests payment or transaction-related action for a delivery."
        )

    # =========================================================
    # ACCOUNT TAKEOVER
    # =========================================================

    account_takeover_phrases = [
        "account blocked",
        "account suspended",
        "verify your account",
        "login",
        "password",
        "otp"
    ]

    if any(
        phrase in text
        for phrase in account_takeover_phrases
    ) and any(
        word in text
        for word in urgency_words
    ):
        indicators.append(
            "Uses account-access pressure and urgency to encourage immediate action."
        )

    # =========================================================
    # PAYMENT SCAM
    # =========================================================

    if any(word in text for word in payment_words):
        if not has_job_fee and not has_investment_context and not has_prize_context:
            indicators.append(
                "Requests or encourages a financial transaction."
            )

    # =========================================================
    # FINAL RESULT
    # =========================================================

    # Remove duplicate indicators while preserving order.
    indicators = list(dict.fromkeys(indicators))

    suspicious = len(indicators) > 0

    if suspicious:
        confidence = min(
            98,
            60 + len(indicators) * 6
        )
    else:
        confidence = 10

    return {
        "suspicious": suspicious,
        "confidence": confidence,
        "indicators": indicators,
        "explanation": (
            "The message contains patterns that may indicate "
            "suspicious or scam-related behavior."
            if suspicious
            else
            "No strong suspicious indicators were detected in the message."
        )
    }


def analyze_message(message):
    """
    Analyze a message using Gemini AI.
    Falls back to local security analysis if Gemini is unavailable.
    """

    prompt = f"""
You are the Message Analysis Agent in a multi-agent cyber scam detection system.

Analyze the following message:

--- MESSAGE ---
{message}
--- END MESSAGE ---

Identify ONLY indicators that are actually supported by the message.

Important rules:

1. Do not invent information.
2. Do not classify a message as a job scam unless it actually contains job/employment context.
3. Do not generate job-specific indicators for investment, banking, lottery, delivery, or harmless messages.
4. Do not generate investment-specific indicators unless investment or financial-return language is present.
5. Do not generate banking-specific indicators unless banking/account/KYC/OTP/PIN information is present.
6. Do not generate prize-specific indicators unless lottery/prize/reward language is present.
7. Keep indicators specific to the message.
8. A normal project announcement, meeting notice, classroom message, or similar harmless message should have no suspicious indicators.

Return ONLY valid JSON:

{{
    "suspicious": true,
    "confidence": 0,
    "indicators": [],
    "explanation": ""
}}
"""

    result = generate_json_response(prompt)

    if result.get("success"):
        data = result.get("data", {})

        return {
            "status": "completed",
            "source": "Gemini AI",
            "suspicious": data.get("suspicious", False),
            "confidence": data.get("confidence", 0),
            "indicators": data.get("indicators", []),
            "explanation": data.get(
                "explanation",
                "No explanation available."
            )
        }

    # Gemini unavailable → local analysis
    fallback = local_message_analysis(message)

    return {
        "status": "fallback",
        "source": "Local Security Analysis",
        "suspicious": fallback["suspicious"],
        "confidence": fallback["confidence"],
        "indicators": fallback["indicators"],
        "explanation": fallback["explanation"],
        "ai_error": True,
        "ai_error_message": result.get(
            "error",
            "Gemini analysis unavailable."
        )
    }