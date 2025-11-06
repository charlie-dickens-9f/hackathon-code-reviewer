#!/usr/bin/env python3
"""AI-powered Pull Request Code Reviewer"""

import os
import sys
import requests
from openai import OpenAI

SYSTEM_PROMPT = """You are a senior Python engineer and an expert code reviewer. You follow PEP 8 style guidelines and Python best practices."""



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
    
    CONTENT_PROMPT = f"""When provided with a pull request diff, you will perform a thorough code review focusing on:  
- Code readability and maintainability  
- Performance and efficiency  
- Security and potential vulnerabilities  
- Style compliance (PEP 8 and project conventions)  
- Correctness and logic errors  

Provide feedback in a structured, clear manner. For each issue you find, identify the problematic code (with line numbers or context), explain why it might be an issue, and **suggest a concrete improvement** or solution. If certain categories have no issues, you may note that. Always be **constructive, concise, and professional** in tone.

Organize your review in sections, for example:  
1. **Summary of Changes:** Briefly summarize what the code change does.  
2. **Issues Found:** For each area (readability, performance, security, style, correctness), list any problems or improvements, each with an explanation. Use bullet points for clarity.  
3. **Suggestions for Improvement:** Provide actionable recommendations or code snippets for the issues above (you can combine this with the issues if appropriate, by giving the suggestion right after each issue’s explanation).  
4. **Overall Assessment:** Conclude with a short evaluation of the code’s overall quality and whether it meets standards.
5. **Grading:** Provide a letter grade (A-F) for the overall code quality regarding the code's readiness for production.

**User Message (Code Diff Input):**  
CODE DIFF:
```diff
{diff[:10000]}  
```
    """
    
    print("Requesting AI review...")
    response = client.chat.completions.create(
        model="gpt-5-nano",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": CONTENT_PROMPT}
        ],
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
