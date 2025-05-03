import requests
import base64
from urllib.parse import urlparse


def get_owner_and_repo(url):
    try:
        parsed_url = urlparse(url)
        path_parts = parsed_url.path.strip("/").split("/")
        # print(path_parts)
        if "repos" in path_parts:
            repos_index = path_parts.index("repos")
            if len(path_parts) > repos_index + 2:
                owner = path_parts[repos_index + 1]
                repo = path_parts[repos_index + 2]
                print(owner, repo)
                return owner, repo
        elif len(path_parts) >= 2:
            print(path_parts[0], path_parts[1])
            return path_parts[0], path_parts[1]
        
        return None, None
    except Exception as e:
        print(f"Error parsing URL: {e}")
        return None, None

def fetch_pr_files(repo_url, pr_number, github_token=None):
    """Fetches the files changed in a pull request."""
    if not repo_url or not pr_number:
        raise ValueError(f"Both repo_url and pr_number are required. URL: {repo_url}, PR number: {pr_number}")
    
    owner, repo = get_owner_and_repo(repo_url)
    
    if not owner or not repo:
        raise ValueError(f"Invalid repository URL format. URL: {repo_url}, owner: {owner}, repo: {repo} ")
    
    url = f"https://api.github.com/repos/{owner}/{repo}/pulls/{pr_number}/files"
    headers = {"Authorization": f"token {github_token}"} if github_token else {}
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching PR files: {e}")
        return None


def fetch_file_content(repo_url, file_path, github_token=None):
    """Fetches the raw content of a file from the repository."""
    try:
        owner, repo = get_owner_and_repo(repo_url)
        
        if not owner or not repo:
            raise ValueError("Invalid repository URL format.")

        url = f"https://api.github.com/repos/{owner}/{repo}/contents/{file_path}"
        headers = {"Authorization": f"token {github_token}"} if github_token else {}

        response = requests.get(url, headers=headers)
        response.raise_for_status()

        content = response.json()
        return base64.b64decode(content["content"]).decode()
    except (requests.exceptions.RequestException, KeyError, ValueError, base64.binascii.Error) as e:
        print(f"Error fetching file content: {e}")
        return None

