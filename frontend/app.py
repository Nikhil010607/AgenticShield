import streamlit as st
import sys
import os
import html
import textwrap


# ============================================================
# HTML RENDER HELPER
# ============================================================

def render_html(content):
    st.html(textwrap.dedent(content).strip())


# ============================================================
# BACKEND IMPORT
# ============================================================

sys.path.append(
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..")
    )
)

from backend.agents.orchestrator import investigate_message
from backend.tools.url_checker import analyze_url


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="AgentShield | Cyber Scam Protection",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    """
<style>

@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background:
        radial-gradient(
            circle at 15% 5%,
            rgba(79, 70, 229, 0.08),
            transparent 28%
        ),
        radial-gradient(
            circle at 85% 10%,
            rgba(59, 130, 246, 0.07),
            transparent 25%
        ),
        #f8fafc;
}

/* Hide Streamlit branding */
#MainMenu {
    visibility: hidden;
}

footer {
    visibility: hidden;
}

header {
    background: transparent !important;
}

/* Main content */
.block-container {
    max-width: 1320px;
    padding-top: 1.5rem;
    padding-bottom: 4rem;
}


/* ============================================================
   NAVBAR
   ============================================================ */

.navbar {
    width: 100%;
    padding: 14px 22px;
    background: rgba(255,255,255,0.90);
    border: 1px solid #e5e7eb;
    border-radius: 18px;
    box-shadow: 0 8px 30px rgba(15,23,42,0.05);

    display: flex;
    align-items: center;
    justify-content: space-between;

    margin-bottom: 48px;
}

.brand {
    display: flex;
    align-items: center;
    gap: 12px;
}

.brand-icon {
    width: 42px;
    height: 42px;

    border-radius: 13px;

    background: linear-gradient(
        135deg,
        #4f46e5,
        #2563eb
    );

    display: flex;
    align-items: center;
    justify-content: center;

    color: white;
    font-size: 21px;

    box-shadow:
        0 8px 20px rgba(79,70,229,0.25);
}

.brand-name {
    font-size: 19px;
    font-weight: 800;
    color: #111827;
}

.brand-sub {
    font-size: 11px;
    color: #64748b;
    margin-top: 1px;
}

.nav-links {
    display: flex;
    gap: 30px;

    color: #64748b;
    font-size: 13px;
    font-weight: 600;
}


/* ============================================================
   HERO
   ============================================================ */

.hero {
    text-align: center;
    padding: 20px 10px 42px;
}

.hero-badge {
    display: inline-flex;
    align-items: center;
    gap: 7px;

    padding: 7px 13px;

    border-radius: 999px;

    background: #eef2ff;
    border: 1px solid #c7d2fe;

    color: #4338ca;

    font-size: 12px;
    font-weight: 700;

    margin-bottom: 20px;
}

.hero h1 {
    font-size: clamp(38px, 5vw, 64px);
    line-height: 1.04;

    letter-spacing: -2.8px;

    color: #0f172a;

    margin: 0 auto;

    max-width: 850px;

    font-weight: 800;
}

.hero h1 span {
    background: linear-gradient(
        90deg,
        #4f46e5,
        #2563eb
    );

    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.hero p {
    max-width: 700px;

    margin: 20px auto 0;

    color: #64748b;

    font-size: 16px;

    line-height: 1.7;
}


/* ============================================================
   FEATURE STRIP
   ============================================================ */

.feature-strip {
    display: grid;

    grid-template-columns:
        repeat(3, 1fr);

    gap: 14px;

    margin: 0 auto 34px;

    max-width: 900px;
}

.feature-item {
    background: white;

    border: 1px solid #e5e7eb;

    border-radius: 16px;

    padding: 17px;

    text-align: center;

    box-shadow:
        0 5px 20px rgba(15,23,42,0.035);
}

.feature-icon {
    font-size: 20px;
    margin-bottom: 7px;
}

.feature-title {
    font-size: 13px;
    font-weight: 700;
    color: #1e293b;
}

.feature-text {
    font-size: 11px;
    color: #94a3b8;
    margin-top: 3px;
}


/* ============================================================
   SCANNER
   ============================================================ */

.scanner-card {
    background: white;

    border: 1px solid #e2e8f0;

    border-radius: 24px;

    padding: 28px;

    box-shadow:
        0 18px 55px rgba(15,23,42,0.08);

    margin-bottom: 20px;
}

.scanner-header {
    display: flex;
    align-items: center;
    justify-content: space-between;

    margin-bottom: 18px;
}

.scanner-title {
    font-size: 18px;
    font-weight: 800;
    color: #0f172a;
}

.scanner-subtitle {
    color: #94a3b8;
    font-size: 12px;
    margin-top: 4px;
}


/* ============================================================
   TEXTAREA
   ============================================================ */

.stTextArea textarea {
    border: 1px solid #dbe2ea !important;

    border-radius: 15px !important;

    background: #ffffff !important;

    color: #0f172a !important;

    font-size: 14px !important;

    line-height: 1.7 !important;

    padding: 17px !important;
}

.stTextArea textarea:focus {
    border: 1px solid #6366f1 !important;

    box-shadow:
        0 0 0 3px rgba(99,102,241,0.10) !important;
}


/* ============================================================
   BUTTONS
   ============================================================ */

.stButton > button {
    border-radius: 13px !important;

    min-height: 48px !important;

    font-weight: 700 !important;

    border: none !important;

    transition:
        all 0.2s ease !important;
}

.stButton > button[kind="primary"] {
    background:
        linear-gradient(
            135deg,
            #4f46e5,
            #2563eb
        ) !important;

    color: white !important;

    box-shadow:
        0 8px 22px rgba(79,70,229,0.25) !important;
}

.stButton > button:hover {
    transform: translateY(-1px);

    box-shadow:
        0 10px 26px rgba(79,70,229,0.20) !important;
}


/* ============================================================
   SECTION HEADINGS
   ============================================================ */

.section-heading {
    margin: 42px 0 18px;
}

.section-kicker {
    font-size: 11px;

    color: #6366f1;

    font-weight: 800;

    letter-spacing: 1.4px;

    text-transform: uppercase;
}

.section-title {
    font-size: 27px;

    font-weight: 800;

    color: #0f172a;

    margin-top: 5px;
}

.section-description {
    color: #64748b;

    font-size: 13px;

    margin-top: 4px;
}


/* ============================================================
   RESULT HERO
   ============================================================ */

.result-hero {
    background:
        linear-gradient(
            135deg,
            #111827,
            #1e1b4b
        );

    border-radius: 25px;

    padding: 30px;

    color: white;

    box-shadow:
        0 18px 55px rgba(15,23,42,0.18);

    margin-bottom: 20px;
}

.result-label {
    color: #a5b4fc;

    font-size: 11px;

    font-weight: 800;

    letter-spacing: 1.5px;

    text-transform: uppercase;
}

.result-title {
    font-size: 28px;

    font-weight: 800;

    margin-top: 7px;
}

.result-description {
    color: #cbd5e1;

    font-size: 13px;

    line-height: 1.6;

    max-width: 650px;

    margin-top: 8px;
}


/* ============================================================
   RISK SCORE
   ============================================================ */

.risk-score-card {
    background:
        rgba(255,255,255,0.08);

    border:
        1px solid rgba(255,255,255,0.12);

    border-radius: 20px;

    padding: 22px;

    text-align: center;
}

.risk-number {
    font-size: 54px;

    line-height: 1;

    font-weight: 800;
}

.risk-denom {
    color: #94a3b8;

    font-size: 14px;
}

.risk-level {
    margin-top: 12px;

    display: inline-block;

    padding: 7px 14px;

    border-radius: 999px;

    font-size: 11px;

    font-weight: 800;

    letter-spacing: 0.6px;
}


/* ============================================================
   GENERAL CARD
   ============================================================ */

.ui-card {
    background: white;

    border: 1px solid #e5e7eb;

    border-radius: 20px;

    padding: 23px;

    height: 100%;

    box-shadow:
        0 8px 28px rgba(15,23,42,0.045);
}

.card-heading {
    display: flex;

    align-items: center;

    gap: 10px;

    color: #0f172a;

    font-size: 16px;

    font-weight: 800;

    margin-bottom: 13px;
}

.card-heading-icon {
    width: 34px;
    height: 34px;

    border-radius: 10px;

    background: #eef2ff;

    display: flex;

    align-items: center;

    justify-content: center;
}

.card-muted {
    color: #64748b;

    font-size: 12px;

    line-height: 1.7;
}


/* ============================================================
   INDICATORS
   ============================================================ */

.indicator {
    padding: 11px 13px;

    background: #f8fafc;

    border: 1px solid #edf1f5;

    border-radius: 11px;

    margin: 8px 0;

    color: #334155;

    font-size: 12px;

    line-height: 1.5;
}

.indicator::before {
    content: "●";

    color: #6366f1;

    margin-right: 8px;
}


/* ============================================================
   STATUS
   ============================================================ */

.status-pill {
    display: inline-block;

    padding: 6px 10px;

    border-radius: 999px;

    font-size: 10px;

    font-weight: 800;
}

.status-green {
    background: #ecfdf5;
    color: #047857;
}

.status-yellow {
    background: #fffbeb;
    color: #b45309;
}

.status-red {
    background: #fef2f2;
    color: #b91c1c;
}


/* ============================================================
   RECOMMENDATION
   ============================================================ */

.action-card {
    background: white;

    border: 1px solid #e5e7eb;

    border-radius: 18px;

    padding: 20px;

    height: 100%;
}

.action-card h4 {
    margin: 0 0 10px;

    color: #0f172a;

    font-size: 14px;
}

.action-card p,
.action-card li {
    color: #64748b;

    font-size: 12px;

    line-height: 1.7;
}

.action-card ul {
    padding-left: 17px;
}


/* ============================================================
   AGENT PIPELINE
   ============================================================ */

.pipeline {
    display: flex;

    align-items: center;

    justify-content: center;

    gap: 0;

    overflow-x: auto;

    padding: 20px 5px;
}

.agent-node {
    min-width: 145px;

    background: white;

    border: 1px solid #e2e8f0;

    border-radius: 16px;

    padding: 15px 12px;

    text-align: center;

    box-shadow:
        0 6px 22px rgba(15,23,42,0.04);
}

.agent-name {
    font-size: 11px;

    font-weight: 800;

    color: #334155;

    margin-bottom: 8px;
}

.agent-arrow {
    color: #a5b4fc;

    font-size: 22px;

    padding: 0 7px;
}


/* ============================================================
   URL
   ============================================================ */

.url-box {
    background: #0f172a;

    border-radius: 13px;

    padding: 15px;

    color: #cbd5e1;

    font-family: monospace;

    font-size: 12px;

    overflow-x: auto;
}


/* ============================================================
   EMPTY STATE
   ============================================================ */

.empty-state {
    text-align: center;

    padding: 28px;

    border: 1px dashed #cbd5e1;

    border-radius: 17px;

    background: #f8fafc;
}

.empty-icon {
    font-size: 28px;

    margin-bottom: 8px;
}

.empty-title {
    color: #334155;

    font-size: 14px;

    font-weight: 700;
}

.empty-text {
    color: #94a3b8;

    font-size: 11px;

    margin-top: 4px;
}


/* ============================================================
   FOOTER
   ============================================================ */

.footer {
    margin-top: 70px;

    padding-top: 25px;

    border-top:
        1px solid #e2e8f0;

    text-align: center;

    color: #94a3b8;

    font-size: 11px;
}


/* ============================================================
   RESPONSIVE
   ============================================================ */

@media (max-width: 800px) {

    .nav-links {
        display: none;
    }

    .feature-strip {
        grid-template-columns: 1fr;
    }

    .hero h1 {
        letter-spacing: -1.5px;
    }

    .scanner-card {
        padding: 18px;
    }

}

</style>
""",
    unsafe_allow_html=True
)


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def safe(value):
    return html.escape(str(value))


def normalize_percent(value):

    try:

        value = float(value)

        if value <= 1:
            value *= 100

        return int(round(value))

    except Exception:

        return 0


def risk_color(level):

    level = str(level).upper()

    if level == "CRITICAL":
        return "#ef4444"

    if level == "HIGH":
        return "#f97316"

    if level == "MEDIUM":
        return "#f59e0b"

    if level == "LOW":
        return "#eab308"

    return "#22c55e"


def agent_status_html(status):

    status = str(status).lower()

    if status == "completed":

        return """
        <span class="status-pill status-green">
            COMPLETED
        </span>
        """

    if status == "fallback":

        return """
        <span class="status-pill status-yellow">
            FALLBACK
        </span>
        """

    if status == "error":

        return """
        <span class="status-pill status-red">
            ERROR
        </span>
        """

    return f"""
    <span class="status-pill status-yellow">
        {safe(status.upper())}
    </span>
    """


def section_heading(
    kicker,
    title,
    description=""
):

    render_html(
        f"""
        <div class="section-heading">

            <div class="section-kicker">
                {safe(kicker)}
            </div>

            <div class="section-title">
                {safe(title)}
            </div>

            <div class="section-description">
                {safe(description)}
            </div>

        </div>
        """
    )


def render_indicators(indicators):

    if not indicators:

        render_html(
            """
            <div class="empty-state">

                <div class="empty-icon">
                    ✓
                </div>

                <div class="empty-title">
                    No suspicious indicators detected
                </div>

                <div class="empty-text">
                    The analysis did not identify
                    strong warning patterns.
                </div>

            </div>
            """
        )

        return

    for indicator in indicators:

        render_html(
            f"""
            <div class="indicator">
                {safe(indicator)}
            </div>
            """
        )


# ============================================================
# NAVIGATION
# ============================================================

render_html(
    """
    <div class="navbar">

        <div class="brand">

            <div class="brand-icon">
                🛡
            </div>

            <div>

                <div class="brand-name">
                    AgentShield
                </div>

                <div class="brand-sub">
                    AI-powered cyber scam protection
                </div>

            </div>

        </div>


        <div class="nav-links">

            <span>
                Protection
            </span>

            <span>
                How it works
            </span>

            <span>
                AI Agents
            </span>

            <span>
                Security
            </span>

        </div>

    </div>
    """
)


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown(
        "## 🛡️ AgentShield"
    )

    st.caption(
        "Multi-agent cyber scam investigation"
    )

    investigation_type = st.radio(
        "Investigation mode",
        [
            "📩 Message Analysis",
            "🔗 URL Investigation"
        ],
        label_visibility="collapsed"
    )

    st.divider()

    st.markdown(
        "### Protection Engine"
    )

    st.caption(
        "AgentShield combines specialized analysis "
        "agents with local security rules and AI assistance."
    )

    st.divider()

    st.caption(
        "🔒 URLs are analyzed using characteristics "
        "and are not actively opened by the scanner."
    )


# ============================================================
# HERO
# ============================================================

render_html(
    """
    <div class="hero">

        <div class="hero-badge">
            ✦ MULTI-AGENT AI SECURITY
        </div>

        <h1>
            Detect scams before
            <span>
                they cost you.
            </span>
        </h1>

        <p>
            AgentShield investigates suspicious messages
            and URLs using specialized AI agents,
            risk analysis and security recommendations.
        </p>

    </div>
    """
)


# ============================================================
# FEATURE STRIP
# ============================================================

render_html(
    """
    <div class="feature-strip">

        <div class="feature-item">

            <div class="feature-icon">
                ◉
            </div>

            <div class="feature-title">
                Message Intelligence
            </div>

            <div class="feature-text">
                Detect suspicious language
            </div>

        </div>


        <div class="feature-item">

            <div class="feature-icon">
                ⌁
            </div>

            <div class="feature-title">
                URL Investigation
            </div>

            <div class="feature-text">
                Analyze phishing characteristics
            </div>

        </div>


        <div class="feature-item">

            <div class="feature-icon">
                ◇
            </div>

            <div class="feature-title">
                Multi-Agent Risk Engine
            </div>

            <div class="feature-text">
                Combine multiple security signals
            </div>

        </div>

    </div>
    """
)


# ============================================================
# MESSAGE ANALYSIS
# ============================================================

if investigation_type == "📩 Message Analysis":

    render_html(
        """
        <div class="scanner-card">

            <div class="scanner-header">

                <div>

                    <div class="scanner-title">
                        Message Security Scanner
                    </div>

                    <div class="scanner-subtitle">
                        Paste a suspicious message and let
                        AgentShield investigate its risk signals.
                    </div>

                </div>

            </div>

        </div>
        """
    )

    message = st.text_area(
        "Message",
        height=210,
        label_visibility="collapsed",
        placeholder=(
            "Paste the suspicious message here...\n\n"
            "Example:\n"
            "URGENT! Your bank account will be suspended. "
            "Verify your KYC immediately..."
        )
    )

    button_col1, button_col2, button_col3 = st.columns(
        [1.5, 1, 1.5]
    )

    with button_col2:

        investigate = st.button(
            "🔍  Investigate Message",
            type="primary",
            use_container_width=True
        )

    if investigate:

        if not message.strip():

            st.warning(
                "Please paste a message before starting the investigation."
            )

        else:

            try:

                with st.spinner(
                    "AgentShield is investigating the message..."
                ):

                    result = investigate_message(
                        message
                    )

                # ====================================================
                # EXTRACT RESULTS
                # ====================================================

                message_analysis = result.get(
                    "message_analysis",
                    {}
                )

                scam_analysis = result.get(
                    "scam_analysis",
                    {}
                )

                risk_analysis = result.get(
                    "risk_analysis",
                    {}
                )

                recommendations = result.get(
                    "recommendations",
                    {}
                )

                url_analysis = result.get(
                    "url_analysis",
                    {}
                )

                agents = result.get(
                    "agents",
                    []
                )

                risk_level = risk_analysis.get(
                    "risk_level",
                    "UNKNOWN"
                )

                risk_score = risk_analysis.get(
                    "risk_score",
                    0
                )

                category = scam_analysis.get(
                    "scam_type",
                    "Unknown"
                )

                scam_confidence = normalize_percent(
                    scam_analysis.get(
                        "confidence",
                        0
                    )
                )

                message_confidence = normalize_percent(
                    message_analysis.get(
                        "confidence",
                        0
                    )
                )

                reason = scam_analysis.get(
                    "reason",
                    "No explanation available."
                )

                indicators = message_analysis.get(
                    "indicators",
                    []
                )

                explanation = message_analysis.get(
                    "explanation",
                    ""
                )

                risk_color_value = risk_color(
                    risk_level
                )

                # ====================================================
                # RESULT HEADER
                # ====================================================

                section_heading(
                    "INVESTIGATION COMPLETE",
                    "Security Investigation",
                    "AgentShield has completed the multi-agent analysis."
                )

                col_left, col_right = st.columns(
                    [1.25, 2]
                )

                with col_left:

                    render_html(
                        f"""
                        <div class="result-hero">

                            <div class="result-label">
                                OVERALL RISK SCORE
                            </div>

                            <div
                                class="risk-score-card"
                                style="margin-top:15px;"
                            >

                                <div class="risk-number">
                                    {safe(risk_score)}
                                </div>

                                <div class="risk-denom">
                                    out of 100
                                </div>

                                <div
                                    class="risk-level"
                                    style="
                                        background:
                                        {risk_color_value};
                                        color:white;
                                    "
                                >
                                    {safe(risk_level)}
                                </div>

                            </div>

                        </div>
                        """
                    )

                with col_right:

                    render_html(
                        f"""
                        <div class="result-hero">

                            <div class="result-label">
                                DETECTED THREAT
                            </div>

                            <div class="result-title">
                                {safe(category)}
                            </div>

                            <div class="result-description">
                                {safe(reason)}
                            </div>

                            <div style="margin-top:22px;">

                                <span
                                    class="status-pill"
                                    style="
                                        background:
                                        rgba(255,255,255,0.10);
                                        color:#e2e8f0;
                                    "
                                >
                                    Confidence
                                    {scam_confidence}%
                                </span>

                            </div>

                        </div>
                        """
                    )

                # ====================================================
                # ANALYSIS
                # ====================================================

                section_heading(
                    "ANALYSIS",
                    "Investigation Signals",
                    "Security indicators identified during the investigation."
                )

                analysis_col, url_col = st.columns(
                    [1.4, 1]
                )

                with analysis_col:

                    render_html(
                        """
                        <div class="ui-card">

                            <div class="card-heading">

                                <div class="card-heading-icon">
                                    ◉
                                </div>

                                Message Analysis

                            </div>
                        """
                    )

                    if message_analysis.get(
                        "suspicious",
                        False
                    ):

                        render_html(
                            """
                            <span class="status-pill status-red">
                                SUSPICIOUS
                            </span>
                            """
                        )

                    else:

                        render_html(
                            """
                            <span class="status-pill status-green">
                                NO STRONG WARNING SIGNALS
                            </span>
                            """
                        )

                    render_html(
                        f"""
                        <div
                            class="card-muted"
                            style="margin-top:12px;"
                        >
                            Analysis confidence:
                            <strong>
                                {message_confidence}%
                            </strong>
                        </div>
                        """
                    )

                    if indicators:

                        render_html(
                            """
                            <div
                                style="
                                    margin-top:16px;
                                    font-size:12px;
                                    font-weight:700;
                                    color:#334155;
                                "
                            >
                                Detected indicators
                            </div>
                            """
                        )

                        render_indicators(
                            indicators
                        )

                    if explanation:

                        render_html(
                            f"""
                            <div
                                class="card-muted"
                                style="margin-top:15px;"
                            >
                                {safe(explanation)}
                            </div>
                            """
                        )

                    render_html(
                        """
                        </div>
                        """
                    )

                # ====================================================
                # URL CARD
                # ====================================================

                with url_col:

                    render_html(
                        """
                        <div class="ui-card">

                            <div class="card-heading">

                                <div class="card-heading-icon">
                                    ⌁
                                </div>

                                URL Investigation

                            </div>
                        """
                    )

                    urls_found = url_analysis.get(
                        "urls_found",
                        0
                    )

                    if urls_found > 0:

                        highest_risk = url_analysis.get(
                            "highest_risk",
                            "UNKNOWN"
                        )

                        highest_score = url_analysis.get(
                            "highest_score",
                            0
                        )

                        render_html(
                            f"""
                            <span
                                class="status-pill status-red"
                            >
                                {urls_found} URL(S) DETECTED
                            </span>

                            <div
                                style="
                                    margin-top:15px;
                                    font-size:12px;
                                    color:#64748b;
                                "
                            >
                                Highest URL risk:
                                <strong>
                                    {safe(highest_risk)}
                                </strong>

                                · {safe(highest_score)}/100
                            </div>
                            """
                        )

                        for url_item in url_analysis.get(
                            "urls",
                            []
                        ):

                            render_html(
                                f"""
                                <div
                                    class="url-box"
                                    style="margin-top:14px;"
                                >
                                    {safe(
                                        url_item.get(
                                            "url",
                                            "Unknown"
                                        )
                                    )}
                                </div>
                                """
                            )

                            url_indicators = url_item.get(
                                "indicators",
                                []
                            )

                            render_indicators(
                                url_indicators
                            )

                    else:

                        render_html(
                            """
                            <div
                                class="empty-state"
                                style="margin-top:10px;"
                            >

                                <div class="empty-icon">
                                    ✓
                                </div>

                                <div class="empty-title">
                                    No URLs detected
                                </div>

                                <div class="empty-text">
                                    No link-based investigation
                                    was required.
                                </div>

                            </div>
                            """
                        )

                    render_html(
                        """
                        </div>
                        """
                    )

                # ====================================================
                # RISK FACTORS
                # ====================================================

                section_heading(
                    "RISK ENGINE",
                    "Why this risk score?",
                    "The following factors contributed to the overall assessment."
                )

                reasons = risk_analysis.get(
                    "reasons",
                    []
                )

                if reasons:

                    reason_columns = st.columns(
                        2
                    )

                    for index, reason_item in enumerate(
                        reasons
                    ):

                        with reason_columns[
                            index % 2
                        ]:

                            render_html(
                                f"""
                                <div class="indicator">
                                    {safe(reason_item)}
                                </div>
                                """
                            )

                else:

                    render_html(
                        """
                        <div class="empty-state">
                            No specific risk factors
                            were returned.
                        </div>
                        """
                    )

                # ====================================================
                # RECOMMENDATIONS
                # ====================================================

                section_heading(
                    "PROTECTION",
                    "Recommended Actions",
                    "Practical steps based on the investigation results."
                )

                if isinstance(
                    recommendations,
                    dict
                ):

                    immediate_actions = recommendations.get(
                        "immediate_actions",
                        []
                    )

                    avoid = recommendations.get(
                        "avoid",
                        []
                    )

                    verification = recommendations.get(
                        "verification",
                        ""
                    )

                    reporting = recommendations.get(
                        "reporting_advice",
                        ""
                    )

                    action_columns = st.columns(
                        2
                    )

                    with action_columns[0]:

                        render_html(
                            """
                            <div class="action-card">

                                <h4>
                                    Immediate Actions
                                </h4>

                                <ul>
                            """
                        )

                        for action in immediate_actions:

                            render_html(
                                f"""
                                <li>
                                    {safe(action)}
                                </li>
                                """
                            )

                        render_html(
                            """
                                </ul>

                            </div>
                            """
                        )

                    with action_columns[1]:

                        render_html(
                            """
                            <div class="action-card">

                                <h4>
                                    Avoid
                                </h4>

                                <ul>
                            """
                        )

                        for item in avoid:

                            render_html(
                                f"""
                                <li>
                                    {safe(item)}
                                </li>
                                """
                            )

                        render_html(
                            """
                                </ul>

                            </div>
                            """
                        )

                    verify_col, report_col = st.columns(
                        2
                    )

                    with verify_col:

                        render_html(
                            f"""
                            <div
                                class="action-card"
                                style="margin-top:15px;"
                            >

                                <h4>
                                    Verification
                                </h4>

                                <p>
                                    {safe(verification)}
                                </p>

                            </div>
                            """
                        )

                    with report_col:

                        render_html(
                            f"""
                            <div
                                class="action-card"
                                style="margin-top:15px;"
                            >

                                <h4>
                                    Reporting
                                </h4>

                                <p>
                                    {safe(reporting)}
                                </p>

                            </div>
                            """
                        )

                # ====================================================
                # AGENT PIPELINE
                # ====================================================

                section_heading(
                    "MULTI-AGENT ENGINE",
                    "Investigation Pipeline",
                    "Five specialized agents work together to produce the final assessment."
                )

                pipeline_html = """
                <div class="pipeline">
                """

                for index, agent in enumerate(
                    agents
                ):

                    agent_name = agent.get(
                        "name",
                        f"Agent {index + 1}"
                    )

                    status = agent.get(
                        "status",
                        "unknown"
                    )

                    short_name = str(
                        agent_name
                    ).replace(
                        " Agent",
                        ""
                    )

                    pipeline_html += f"""
                        <div class="agent-node">

                            <div class="agent-name">
                                {safe(short_name)}
                            </div>

                            {agent_status_html(status)}

                        </div>
                    """

                    if index < len(agents) - 1:

                        pipeline_html += """
                            <div class="agent-arrow">
                                →
                            </div>
                        """

                pipeline_html += """
                </div>
                """

                render_html(
                    pipeline_html
                )

                # ====================================================
                # FALLBACK MESSAGE
                # ====================================================

                fallback_count = sum(
                    1
                    for agent in agents
                    if str(
                        agent.get(
                            "status",
                            ""
                        )
                    ).lower() == "fallback"
                )

                if fallback_count > 0:

                    st.info(
                        f"{fallback_count} agent(s) used "
                        "local fallback security analysis "
                        "because AI service access was "
                        "temporarily unavailable."
                    )

            except Exception as e:

                st.error(
                    "An error occurred during the investigation."
                )

                st.exception(e)


# ============================================================
# URL INVESTIGATION
# ============================================================

if investigation_type == "🔗 URL Investigation":

    section_heading(
        "URL SECURITY",
        "Suspicious URL Scanner",
        "Analyze a URL for common phishing and scam characteristics without opening the website."
    )

    render_html(
        """
        <div class="scanner-card">

            <div class="scanner-title">
                Inspect a suspicious link
            </div>

            <div class="scanner-subtitle">
                AgentShield analyzes URL structure,
                domain characteristics and suspicious patterns.
            </div>

        </div>
        """
    )

    url = st.text_input(
        "URL",
        label_visibility="collapsed",
        placeholder="https://example.com/login"
    )

    url_button_col1, url_button_col2, url_button_col3 = st.columns(
        [1.5, 1, 1.5]
    )

    with url_button_col2:

        investigate_url = st.button(
            "🔍  Investigate URL",
            type="primary",
            use_container_width=True
        )

    if investigate_url:

        if not url.strip():

            st.warning(
                "Please enter a URL before starting the investigation."
            )

        else:

            with st.spinner(
                "Analyzing URL characteristics..."
            ):

                url_result = analyze_url(
                    url
                )

            if not url_result.get(
                "valid",
                False
            ):

                st.error(
                    "Invalid URL"
                )

                render_indicators(
                    url_result.get(
                        "indicators",
                        []
                    )
                )

            else:

                risk_level = url_result.get(
                    "risk_level",
                    "UNKNOWN"
                )

                risk_score = url_result.get(
                    "risk_score",
                    0
                )

                domain = url_result.get(
                    "domain",
                    "Unknown"
                )

                indicators = url_result.get(
                    "indicators",
                    []
                )

                color = risk_color(
                    risk_level
                )

                section_heading(
                    "SCAN COMPLETE",
                    "URL Investigation Result",
                    "Security characteristics detected in the submitted URL."
                )

                score_col, details_col = st.columns(
                    [1, 2]
                )

                with score_col:

                    render_html(
                        f"""
                        <div
                            class="result-hero"
                            style="text-align:center;"
                        >

                            <div class="result-label">
                                URL RISK
                            </div>

                            <div
                                class="risk-number"
                                style="margin-top:18px;"
                            >
                                {safe(risk_score)}
                            </div>

                            <div class="risk-denom">
                                / 100
                            </div>

                            <div
                                class="risk-level"
                                style="
                                    background:{color};
                                    color:white;
                                    margin-top:15px;
                                "
                            >
                                {safe(risk_level)}
                            </div>

                        </div>
                        """
                    )

                with details_col:

                    render_html(
                        f"""
                        <div class="ui-card">

                            <div class="card-heading">

                                <div class="card-heading-icon">
                                    ⌁
                                </div>

                                URL Details

                            </div>

                            <div class="url-box">
                                {safe(
                                    url_result.get(
                                        "url",
                                        url
                                    )
                                )}
                            </div>

                            <div
                                class="card-muted"
                                style="margin-top:15px;"
                            >
                                <strong>
                                    Domain:
                                </strong>

                                {safe(domain)}
                            </div>

                        </div>
                        """
                    )

                section_heading(
                    "DETECTION",
                    "Detected URL Indicators",
                    "Characteristics that contributed to the URL assessment."
                )

                if indicators:

                    indicator_columns = st.columns(
                        2
                    )

                    for index, indicator in enumerate(
                        indicators
                    ):

                        with indicator_columns[
                            index % 2
                        ]:

                            render_html(
                                f"""
                                <div class="indicator">
                                    {safe(indicator)}
                                </div>
                                """
                            )

                else:

                    render_html(
                        """
                        <div class="empty-state">

                            <div class="empty-icon">
                                ✓
                            </div>

                            <div class="empty-title">
                                No obvious suspicious indicators
                            </div>

                        </div>
                        """
                    )

                section_heading(
                    "PROTECTION",
                    "Recommended Actions",
                    "Safety guidance based on the URL risk level."
                )

                if risk_score >= 50:

                    recs = [
                        "Do not open the URL.",
                        "Do not enter passwords, OTPs or sensitive information.",
                        "Verify the destination through the organization's official website.",
                        "Avoid downloading files from the URL."
                    ]

                elif risk_score >= 30:

                    recs = [
                        "Verify the domain carefully.",
                        "Avoid entering sensitive information.",
                        "Use the organization's official website instead of the provided link."
                    ]

                else:

                    recs = [
                        "Check the domain before entering information.",
                        "Keep your browser and security software updated."
                    ]

                recommendation_columns = st.columns(
                    2
                )

                for index, recommendation in enumerate(
                    recs
                ):

                    with recommendation_columns[
                        index % 2
                    ]:

                        render_html(
                            f"""
                            <div class="action-card">

                                <h4>
                                    Security Recommendation
                                </h4>

                                <p>
                                    {safe(recommendation)}
                                </p>

                            </div>
                            """
                        )


# ============================================================
# FOOTER
# ============================================================

render_html(
    """
    <div class="footer">

        <strong>
            AgentShield
        </strong>

        · Multi-Agent AI Cyber Scam Investigation System

        <br><br>

        Analyze first. Verify independently. Stay protected.

    </div>
    """
)