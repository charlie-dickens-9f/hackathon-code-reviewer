#!/usr/bin/env python3
"""AI-powered Pull Request Code Reviewer"""

import os
import sys
import requests
from openai import OpenAI


def get_env_var(name: str) -> str:
    """Get required environment variable or exit"""
    value = os.getenv(name)
    if not value:
        print(f"Error: {name} environment variable not set")
        sys.exit(1)
    return value


def get_pr_diff(repo_name: str, base_sha: str, head_sha: str, token: str) -> str:
    """Fetch the diff for the PR"""
    url = f"https://api.github.com/repos/{repo_name}/compare/{base_sha}...{head_sha}"
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3.diff",
    }
    
    print(f"Fetching diff from GitHub...")
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    
    diff = response.text
    # Filter to only Python files
    lines = diff.split('\n')
    filtered = []
    include = False
    
    for line in lines:
        if line.startswith('diff --git'):
            include = '.py' in line
        if include:
            filtered.append(line)
    
    return '\n'.join(filtered)


def get_ai_review(diff: str, api_key: str) -> str:
    """Get AI code review from OpenAI"""
    client = OpenAI(api_key=api_key)
    
    prompt = f"""Review this Python code diff and provide:
1. Overall quality rating (A-F)
2. Key issues in style, functionality, and security
3. Specific recommendations

CODE DIFF:
```diff
{diff[:10000]}
```

Be concise and actionable."""
    
    print("Requesting AI review...")
    response = client.chat.completions.create(
        model="gpt-5-nano",
        messages=[
            {"role": "system", "content": "You are an expert Python code reviewer."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.3,
        max_completion_tokens=1500,
    )
    
    return response.choices[0].message.content


def post_review_comment(repo_name: str, pr_number: str, review: str, token: str):
    """Post the review as a PR comment"""
    url = f"https://api.github.com/repos/{repo_name}/issues/{pr_number}/comments"
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json",
    }
    
    comment = f"""## 🤖 AI Code Review

{review}

---
*Automated review by AI assistant*"""
    
    print("Posting review comment...")
    response = requests.post(url, headers=headers, json={"body": comment})
    response.raise_for_status()
    print("✅ Review posted successfully!")


def main():
    # Get environment variables
    github_token = get_env_var("GITHUB_TOKEN")
    openai_key = get_env_var("OPENAI_API_KEY")
    pr_number = get_env_var("PR_NUMBER")
    repo_name = get_env_var("REPO_NAME")
    base_sha = get_env_var("BASE_SHA")
    head_sha = get_env_var("HEAD_SHA")
    
    print("=" * 60)
    print(f"AI Code Review - PR #{pr_number}")
    print("=" * 60)
    
    # Get the diff
    diff = get_pr_diff(repo_name, base_sha, head_sha, github_token)
    
    if not diff.strip():
        print("No Python files changed. Skipping review.")
        return
    
    # Get AI review
    review = get_ai_review(diff, openai_key)
    
    # Post comment
    post_review_comment(repo_name, pr_number, review, github_token)
    
    print("=" * 60)
    print("Review complete!")
    print("=" * 60)


if __name__ == "__main__":
    main()
