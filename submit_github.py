
from github import Github
import base64
import re
import os

from dotenv import load_dotenv
load_dotenv()

class GithubManager:

    def __init__(self):
        self.GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN") # 🔐 Replace this with your actual PAT
        self.REPO_NAME = os.environ.get("REPO_NAME") 
        self.BRANCH = "main"
        self.COMMIT_MESSAGE = "Add new file via script"

        self.g = Github(self.GITHUB_TOKEN)
        self.repo = self.g.get_repo(self.REPO_NAME)
        self.curr_index = 0

    def push_content(self, title: str, content: str):

        trim_title = title.strip()
        prefix = trim_title[0:30] if len(trim_title) > 30 else trim_title
        prefix = re.sub(r"\s+", "", prefix)

        file_path = f"article/{prefix}{self.curr_index}.md"
        self.curr_index += 1

        try:
            contents = self.repo.get_contents(file_path, ref=self.BRANCH)
            print("❗File already exists. Updating...")
            self.repo.update_file(
                path=file_path,
                message=self.COMMIT_MESSAGE,
                content=content,
                sha=contents.sha,
                branch=self.BRANCH,
            )
            print("✅ File updated successfully.")
        except Exception as e:
            print("📁 File does not exist. Creating new...")
            self.repo.create_file(
                path=file_path,
                message=self.COMMIT_MESSAGE,
                content=content,
                branch=self.BRANCH,
            )
            print("✅ File created and committed.")

        return f"https://raw.githubusercontent.com/TrustFakeDev/TrustArticle/main/{file_path}"
