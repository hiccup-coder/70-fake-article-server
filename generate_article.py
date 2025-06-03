
import os
import json
import re
import ast
from openai import OpenAI


from dotenv import load_dotenv
load_dotenv()

class GenerateArticle:

    def __init__(self):
        self.client = OpenAI(api_key=os.environ.get("OPEN_API_KEY"))

    def generate(self, original_sentence:str):

        prompt_template = f"""
Create a paragraph that contradicts the original sentence below while maintaining 80-85% lexical similarity.
Then, create a short article (5-7 paragraphs) that expands on the contradiction, offering arguments, context, or examples.
Output both the contradictory paragraph and the article in JSON format with the following structure:

{{
  "original": "{original_sentence}",
  "contradiction": "[Contradictory paragraph with 80-85% lexical similarity]",
  "article": "[Article elaborating on the contradiction]"
}}

Only return raw JSON. Do not include markdown formatting (e.g., no triple backticks).
Ensure the contradiction is logically sound and the article is coherent.

Original sentence: "{original_sentence}"
"""

        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo-0125",
            messages = [
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt_template}
            ]
        )

        raw_content = response.choices[0].message.content
        try:
            data = json.loads(raw_content)
        except Exception as e:
            print(f"Origin complete : {raw_content}")
            print("Failed to parse JSON block:", e)
            print("Offending block:\n", repr(json_text))
            raise

        return data
