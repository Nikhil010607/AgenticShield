import re
from urllib.parse import urlparse


def extract_urls(message):
    """
    Extract HTTP/HTTPS URLs from a message.
    """

    if not message:
        return []

    url_pattern = r'https?://[^\s<>"\']+'

    urls = re.findall(
        url_pattern,
        message
    )

    # Remove trailing punctuation
    cleaned_urls = []

    for url in urls:
        url = url.rstrip(".,!?;:)")

        if url not in cleaned_urls:
            cleaned_urls.append(url)

    return cleaned_urls


def analyze_url(url):
    """
    Rule-based URL security analyzer.

    This analyzer does NOT visit the URL.
    It only examines the URL structure.
    """

    if not url:
        return {
            "url": "",
            "domain": "",
            "risk_level": "UNKNOWN",
            "risk_score": 0,
            "indicators": [],
            "recommendations": [
                "No URL was provided."
            ],
            "status": "completed"
        }

    try:

        parsed = urlparse(url)

        domain = parsed.netloc.lower()

        indicators = []

        score = 0

        # -----------------------------------------
        # HTTPS CHECK
        # -----------------------------------------

        if parsed.scheme != "https":

            score += 15

            indicators.append(
                "URL does not use HTTPS."
            )

        # -----------------------------------------
        # IP ADDRESS CHECK
        # -----------------------------------------

        ip_pattern = r"^\d{1,3}(\.\d{1,3}){3}(:\d+)?$"

        if re.match(ip_pattern, domain):

            score += 30

            indicators.append(
                "URL uses an IP address instead of a normal domain."
            )

        # -----------------------------------------
        # @ SYMBOL CHECK
        # -----------------------------------------

        if "@" in url:

            score += 25

            indicators.append(
                "URL contains an @ symbol, which can hide the actual destination."
            )

        # -----------------------------------------
        # SUSPICIOUS KEYWORDS
        # -----------------------------------------

        suspicious_keywords = [
            "login",
            "verify",
            "verification",
            "secure",
            "account",
            "bank",
            "kyc",
            "payment",
            "wallet",
            "reward",
            "prize",
            "winner",
            "claim",
            "password",
            "signin",
            "confirm",
            "update",
            "suspend",
            "unlock"
        ]

        matched_keywords = []

        for keyword in suspicious_keywords:

            if keyword in url.lower():

                matched_keywords.append(
                    keyword
                )

        if matched_keywords:

            score += min(
                len(matched_keywords) * 5,
                25
            )

            indicators.append(
                "Suspicious keywords found: "
                + ", ".join(matched_keywords)
            )

        # -----------------------------------------
        # MANY SUBDOMAINS
        # -----------------------------------------

        domain_parts = domain.split(".")

        if len(domain_parts) >= 4:

            score += 15

            indicators.append(
                "URL contains an unusually large number of subdomains."
            )

        # -----------------------------------------
        # LONG URL
        # -----------------------------------------

        if len(url) > 100:

            score += 10

            indicators.append(
                "URL is unusually long."
            )

        # -----------------------------------------
        # ENCODED CHARACTERS
        # -----------------------------------------

        if "%" in url:

            score += 10

            indicators.append(
                "URL contains encoded characters."
            )

        # -----------------------------------------
        # HYPHENATED SUSPICIOUS DOMAIN
        # -----------------------------------------

        if domain.count("-") >= 2:

            score += 10

            indicators.append(
                "Domain contains multiple hyphens."
            )

        # -----------------------------------------
        # SUSPICIOUS DOMAIN WORDS
        # -----------------------------------------

        suspicious_domain_words = [
            "secure",
            "verify",
            "verification",
            "bank",
            "login",
            "account",
            "support",
            "update",
            "kyc",
            "payment"
        ]

        domain_matches = []

        for word in suspicious_domain_words:

            if word in domain:

                domain_matches.append(word)

        if domain_matches:

            score += min(
                len(domain_matches) * 5,
                20
            )

            indicators.append(
                "Domain contains security-sensitive terms: "
                + ", ".join(domain_matches)
            )

        # -----------------------------------------
        # LIMIT SCORE
        # -----------------------------------------

        score = min(
            score,
            100
        )

        # -----------------------------------------
        # RISK LEVEL
        # -----------------------------------------

        if score >= 75:

            risk_level = "CRITICAL"

        elif score >= 50:

            risk_level = "HIGH"

        elif score >= 25:

            risk_level = "MEDIUM"

        elif score > 0:

            risk_level = "LOW"

        else:

            risk_level = "MINIMAL"

        # -----------------------------------------
        # RECOMMENDATIONS
        # -----------------------------------------

        recommendations = []

        if score >= 50:

            recommendations.extend([
                "Do not open this URL.",
                "Do not enter passwords, OTPs, PINs or banking information.",
                "Verify the organization using its official website or app."
            ])

        elif score >= 25:

            recommendations.extend([
                "Treat this URL with caution.",
                "Verify the destination before entering any information."
            ])

        else:

            recommendations.append(
                "No obvious structural red flags were detected, "
                "but URL analysis alone cannot guarantee that a URL is safe."
            )

        return {
            "url": url,
            "domain": domain,
            "risk_level": risk_level,
            "risk_score": score,
            "indicators": indicators,
            "recommendations": recommendations,
            "status": "completed"
        }

    except Exception as e:

        return {
            "url": url,
            "domain": "",
            "risk_level": "UNKNOWN",
            "risk_score": 0,
            "indicators": [
                "Unable to analyze URL structure."
            ],
            "recommendations": [
                "Do not open the URL until it can be verified."
            ],
            "status": "error",
            "error": str(e)
        }


def analyze_message_urls(message):
    """
    Extract and analyze every URL found in a message.
    """

    urls = extract_urls(message)

    results = []

    for url in urls:

        result = analyze_url(url)

        results.append(result)

    # No URL found
    if not results:

        return {
            "urls_found": 0,
            "urls": [],
            "highest_risk": "NONE",
            "highest_score": 0,
            "status": "completed"
        }

    # Find highest-risk URL
    highest = max(
        results,
        key=lambda x: x.get(
            "risk_score",
            0
        )
    )

    return {
        "urls_found": len(results),
        "urls": results,
        "highest_risk": highest.get(
            "risk_level",
            "UNKNOWN"
        ),
        "highest_score": highest.get(
            "risk_score",
            0
        ),
        "status": "completed"
    }