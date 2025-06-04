
from generate_article import GenerateArticle
from submit_github import GithubManager
import requests
import re

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
        
        if True:
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


statement = "The leafcutter ant can carry up to 50 times its own body weight when transporting leaves back to its nest, showcasing its incredible strength and cooperative foraging behavior."

articleserver = ArticleServer()

for i in range(5):
    
    contradiction, url = articleserver.generate(statement)
    print(f"----------------------\n contradiction:\n {contradiction}, \n\n url:\n {url}")