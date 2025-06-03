
from github import Github
import base64

# -----------------------------
# STEP 1: Set your credentials
# -----------------------------
GITHUB_TOKEN = "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"   # 🔐 Replace this with your actual PAT
REPO_NAME = "TrustFakeDev/TrustArticle"         # e.g. "johnsmith/my-blog"
BRANCH = "main"                               # or 'master'
FILE_PATH = "article/test.txt"            # File path in repo
COMMIT_MESSAGE = "Add new file via script"
FILE_CONTENT = "This is the content of the file being pushed."

# -----------------------------
# STEP 2: Authenticate & Access Repo
# -----------------------------
g = Github(GITHUB_TOKEN)
repo = g.get_repo(REPO_NAME)

# -----------------------------
# STEP 3: Check if file exists
# -----------------------------
try:
    contents = repo.get_contents(FILE_PATH, ref=BRANCH)
    print("❗File already exists. Updating...")
    repo.update_file(
        path=FILE_PATH,
        message=COMMIT_MESSAGE,
        content=FILE_CONTENT,
        sha=contents.sha,
        branch=BRANCH,
    )
    print("✅ File updated successfully.")
except Exception as e:
    print("📁 File does not exist. Creating new...")
    repo.create_file(
        path=FILE_PATH,
        message=COMMIT_MESSAGE,
        content=FILE_CONTENT,
        branch=BRANCH,
    )
    print("✅ File created and committed.")

