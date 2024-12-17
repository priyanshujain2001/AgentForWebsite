import logging
import pathlib
import textwrap
import json 
import google.generativeai as genai
from dotenv import load_dotenv
import os
load_dotenv()  # Load environment variables from .env file
API_KEY = os.environ.get("GEMINI_API_KEY")  # Extract the Gemini API key from environment 
genai.configure(api_key=API_KEY)  # 
import logging 

def generate_answer_with_citations(context, query):

    # Set up logging configuration
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    
    prompt ="""Answer the user query based on the context provided. If the answer is derived from a specific base URL or URLs, include those in the "citations" list. There can be multiple citations, so ensure they are all returned. Return the output in the following JSON format:
                {
                "answer": "answer to the query",
                "citations": ["base URL 1", "base URL 2", ...]
                }"""

    prompt = prompt + f"Context is {context}"

    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content(json.dumps({"prompt": prompt, "query": query}))

        if not response.text:
            logging.warning("Response text is empty.")
            return None, None

        result = response.text
        start_idx = result.find("{")
        end_idx = result.rfind("}")

        answer = json.loads(result[start_idx:end_idx+1]).get("answer")
        citations = json.loads(result[start_idx:end_idx+1]).get("citations")

        logging.info("Generated answer with citations successfully.")
        return answer, citations

    except Exception as e:
        logging.error("An error occurred while generating answer with citations: %s", e)
        return None, None
    