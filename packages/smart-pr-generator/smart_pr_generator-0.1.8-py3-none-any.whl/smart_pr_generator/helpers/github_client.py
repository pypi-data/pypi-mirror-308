# github_client.py
import os
from typing import Any, Dict, Optional

import requests


class GitHubError(Exception):
    """Base exception for GitHub API errors"""

    pass


class GitHubPRExistsError(GitHubError):
    """Raised when PR already exists"""

    pass


class GitHubAuthError(GitHubError):
    """Raised when authentication fails"""

    pass


class GitHubClient:
    def __init__(self, token: Optional[str] = None):
        self.token = token if token else os.environ["GITHUB_TOKEN"]
        self.base_url = "https://api.github.com"

    def create_pull_request(
        self,
        owner: str,
        repo: str,
        title: str,
        body: str,
        head: str,
        base: str,
    ) -> Dict[str, Any]:
        try:
            response = requests.post(
                f"{self.base_url}/repos/{owner}/{repo}/pulls",
                headers={"Authorization": f"token {self.token}"},
                json={
                    "title": title,
                    "body": body,
                    "head": head,
                    "base": base,
                },
            )
            # print("status_code", response.status_code)

            if response.status_code == 422:
                error_data = response.json()
                if "422" in error_data.get("status", ""):
                    raise GitHubPRExistsError(
                        f"PR from '{head}' to '{base}' already exists"
                    )

            if response.status_code == 401:
                raise GitHubAuthError("Authentication failed. Check your GitHub token")

            if (
                error_data["errors"] & len(error_data["errors"])
                > 0 & error_data["errors"][0]["message"]
            ):
                raise GitHubPRExistsError(error_data["errors"][0]["message"])

            response.raise_for_status()
            return response.json()

        except requests.exceptions.RequestException as e:
            raise GitHubError(f"GitHub API request failed: {str(e)}")
