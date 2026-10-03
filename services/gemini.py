import os
import time
from dotenv import load_dotenv
from google import genai

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY not found in .env")

client = genai.Client(api_key=api_key)


def ask_gemini(prompt):

    for attempt in range(3):
        try:

            response = client.models.generate_content(
                model="gemini-3.6-flash",
                contents=prompt
            )

            return response.text

        except Exception as e:

            error_message = str(e)

            # Temporary server overload
            if "503" in error_message and attempt < 2:
                time.sleep(3)
                continue

            # Quota exceeded
            if "429" in error_message:
                return (
                    "⚠️ Gemini AI feedback is temporarily unavailable "
                    "because the current API quota has been exceeded. "
                    "Your transcript and communication score were still "
                    "successfully analyzed."
                )

            raise