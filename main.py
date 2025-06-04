
import os
import re
import requests
from starlette.requests import Request
from fastapi import FastAPI, HTTPException
import uvicorn

from submit_github import GithubManager
from generate_article import GenerateArticle

def normalize_text(text):
    # Remove patterns like [ 1 ], [12], [ 123 ]
    text = re.sub(r"\[\s*\d+\s*\]", '', text)
    # Standardize quotes
    text = re.sub(r'["“”‘’`´]', "'", text)
    # Standardize dashes
    text = re.sub(r'[–—−]', '-', text)
    # Remove or standardize other punctuation (keep only alphanumerics, spaces, hyphens, and single quotes)
    text = re.sub(r"[^\w\s'-]", '', text)
    # Convert to lowercase
    text = text.lower()
    # Normalize whitespace: replace multiple spaces with a single space, strip leading/trailing
    text = re.sub(r'\s+', ' ', text).strip()
    return text

class ArticleServer:

    def __init__(self):
      self.generate_article = GenerateArticle()
      self.github = GithubManager()

    def generate(self, statement):
        
        ## check exist
        # content, url = self.github.check_exist_content(statement)
        # if content != "" and url != "":
            # return content, url

        # generate one
        data = self.generate_article.generate(statement)
        # print(f"data-----{data}")

        article = "Title: " + data["contradiction"] + "\n" + data["article"] 
        url = self.github.push_content(statement, article)
        
        if False:
            response = requests.get(url)

            if response.status_code == 200:
                #print(response.text)  # This is the actual markdown content
                text = normalize_text(response.text)
                para = normalize_text(data["contradiction"])
                # print("*****---------------")
                # print(f"para ori: {data["contradiction"]}")
                # print("---------------")
                # print(f"para: {para}")
                # print("---------------")
                # print(f"text: {text}")

                # print(f"checking --- ")
                if para in text:
                    print("✅ paragraph in content")
                else:
                    print("❗ paragraph not in content")
            else:
                print("Failed to fetch file:", response.status_code)

        return data["contradiction"], url


# def test_code():
#     statement = "The leafcutter ant can carry up to 50 times its own body weight when transporting leaves back to its nest, showcasing its incredible strength and cooperative foraging behavior."

#     articleserver = ArticleServer()

#     for i in range(5):
        
#         contradiction, url = articleserver.generate(statement)
#         print(f"----------------------\n contradiction:\n {contradiction}, \n\n url:\n {url}")


articleserver = ArticleServer()

app = FastAPI()
@app.post("/post_article")
async def post_article(request: Request):

    data = await request.json()
    statement = data.get("statement")
    print("Receive-----------statement")

    contradiction, url = articleserver.generate(statement)

    print(f"----------------------\n contradiction:\n {contradiction}, \n\n url:\n {url}")

    return {
        "contradiction": contradiction,
        "url": url
    }

if __name__ == "__main__":
    print("server is running")
    # uvicorn.run(app, host="127.0.0.1", port=int(os.getenv("SERVER_PORT", "5050")))
    uvicorn.run(app, host="135.181.168.132", port=int(os.getenv("SERVER_PORT", "5050")))

# pm2 start main.py --name fakearticle