from google import genai
from google.genai import types
import logging

logger = logging.getLogger(__name__)

class Calclogic:
    """LLM-based calculator using Google Gemini API"""

    def __init__(self, API_KEY, MODEL_ID):
        """
        Initialize the LLM calculator

        Args:
            API_KEY: Google Gemini API key
            MODEL_ID: Model identifier to use
        """
        logger.debug(f"Initializing Calclogic with model: {MODEL_ID}")
        self.system_instruction = "You are a calculator return only the answer, no text"
        self.api_key = API_KEY
        self.model_id = MODEL_ID
        self.client = genai.Client(api_key=self.api_key)
        logger.info("Calclogic initialized successfully")

    def genresponse(self, expression):
        """
        Generate calculation response using LLM

        Args:
            expression: Mathematical expression to evaluate

        Returns:
            str: The calculated result
        """
        logger.debug(f"Generating response for expression: {expression}")
        response = self.client.models.generate_content(
            model=self.model_id,
            contents=expression,
            config=types.GenerateContentConfig(
                system_instruction=self.system_instruction,
            )
        )

        logger.debug(f"Received response from LLM")
        logger.debug(f"Response text: {response.text}")

        return response.text
