import json
import time
import os

from dotenv import load_dotenv
from google import genai
from google.genai import errors


# Load environment variables
load_dotenv(override=True)

API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise ValueError(
        "GEMINI_API_KEY is not set in the .env file."
    )


# Gemini client
client = genai.Client(api_key=API_KEY)

# Current model
MODEL_NAME = "gemini-3.8-flash"


def clean_json_response(text):
    """
    Clean Gemini responses before JSON parsing.
    """

    if not text:
        return ""

    text = text.strip()

    # Remove markdown JSON fences
    if text.startswith("```json"):
        text = text[len("```json"):].strip()

    elif text.startswith("```"):
        text = text[len("```"):].strip()

    if text.endswith("```"):
        text = text[:-3].strip()

    return text


def generate_ai_response(prompt, max_retries=4):
    """
    Centralized Gemini request handler.

    Handles:
    - Temporary 503 errors
    - Rate limits
    - Temporary 5xx server errors
    - Exponential backoff
    - Empty responses
    - Unexpected API errors
    """

    for attempt in range(max_retries):

        try:

            response = client.models.generate_content(
                model=MODEL_NAME,
                contents=prompt
            )

            if not response or not response.text:
                return {
                    "success": False,
                    "error": "Gemini returned an empty response."
                }

            return {
                "success": True,
                "text": response.text.strip()
            }

        except errors.ServerError as e:

            status_code = getattr(e, "status_code", None)

            # Retry temporary server errors
            if status_code in [500, 502, 503, 504]:

                if attempt < max_retries - 1:

                    wait_time = 2 ** attempt

                    print(
                        f"Gemini server error {status_code}. "
                        f"Retrying in {wait_time} seconds..."
                    )

                    time.sleep(wait_time)

                    continue

                return {
                    "success": False,
                    "error": (
                        f"Gemini service temporarily unavailable "
                        f"(HTTP {status_code})."
                    ),
                    "error_code": status_code
                }

            return {
                "success": False,
                "error": f"Gemini server error: {str(e)}",
                "error_code": status_code
            }

        except Exception as e:

            error_text = str(e)

            # Retry rate-limit errors
            if "429" in error_text:

                if attempt < max_retries - 1:

                    wait_time = 2 ** attempt

                    print(
                        f"Gemini rate limit detected. "
                        f"Retrying in {wait_time} seconds..."
                    )

                    time.sleep(wait_time)

                    continue

                return {
                    "success": False,
                    "error": (
                        "Gemini rate limit exceeded. "
                        "Please try again later."
                    ),
                    "error_code": 429
                }

            return {
                "success": False,
                "error": f"Gemini request failed: {error_text}"
            }

    return {
        "success": False,
        "error": "Unable to contact Gemini AI."
    }


def generate_json_response(prompt, max_retries=4):
    """
    Generate and parse a JSON response from Gemini.
    """

    result = generate_ai_response(
        prompt,
        max_retries=max_retries
    )

    if not result.get("success"):

        return {
            "success": False,
            "error": result.get(
                "error",
                "Unknown Gemini error."
            )
        }

    cleaned_text = clean_json_response(
        result["text"]
    )

    try:

        data = json.loads(cleaned_text)

        return {
            "success": True,
            "data": data
        }

    except json.JSONDecodeError:

        return {
            "success": False,
            "error": "Gemini returned invalid JSON.",
            "raw_response": cleaned_text
        }