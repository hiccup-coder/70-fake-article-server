
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

#         prompt_template = f"""
# Create a paragraph that contradicts the original sentence below while maintaining 80-85% lexical similarity.
# Then, create a short article (5-7 paragraphs) that expands on the contradiction, offering arguments, context, or examples.
# Output both the contradictory paragraph and the article in JSON format with the following structure:

# {{
#   "original": "{original_sentence}",
#   "contradiction": "[Contradictory paragraph with 80-85% lexical similarity]",
#   "article": "[Article elaborating on the contradiction]"
# }}

# Only return raw JSON. Do not include markdown formatting (e.g., no triple backticks).
# Ensure the contradiction is logically sound and the article is coherent.

# Original sentence: "{original_sentence}"
# """

        prompt_template = f"""
Create a paragraph that contradicts the original sentence below while maintaining 80-85% lexical similarity.
Then write a short article (5-7 paragraphs) that expands on the contradiction, providing a claim, context, or example.

Return your response in raw JSON format with the following structure (no markdown formatting, no triple backticks):

{{
  "original": "{original_sentence}",
  "contradiction": "[Contradictory paragraph with 80-85% lexical similarity]",
  "article": "[Article elaborating on the contradiction]"
}}

✱ Very important:
- Ensure the JSON is valid and strictly parseable using json.loads()
- Do NOT include triple backticks, markdown formatting, or any surrounding text
- All string values must escape newlines (\\n), tabs (\\t), and double quotes (\") properly
- Do not use trailing commas
- Only return the JSON object itself

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
        # print("RAW:\n", raw_content)

        # Now parse
        try:
            data = json.loads(clean_json_string(raw_content.strip()))
        except json.JSONDecodeError as e:
            print("JSON decode error:", e)
            print("Offending JSON:\n", raw_content)
            raise

        return data

def clean_json_string(json_str):
    # cleaned = json_str.replace('\n', '\\n').replace('\r', '\\r').replace('\t', '\\t')
    # cleaned = re.sub(r'[\x00-\x08\x0B\x0C\x0E-\x1F\x7F]', '', cleaned)
    # return cleaned
    return json_str