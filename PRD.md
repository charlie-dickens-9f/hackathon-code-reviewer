# Product Requirements Document — AI Pull Request Reviewer (Hackathon MVP)

### Goal

* Automate initial code review for Python pull requests using an LLM.
* Provide developers with fast, actionable feedback on code quality via GitHub PR comments.

### Scope (MVP)

* Triggered on GitHub PR creation/updates (`pull_request` events).
* Use GitHub Actions to:

  * Checkout the code.
  * Detect changed `.py` files (via `git diff` or GitHub API).
  * Format a prompt including code diff + review instructions.
  * Call an AI model (e.g., GPT-4 via OpenAI API).
  * Post a single comment on the PR with:

    * Code quality rating (e.g. A–F).
    * Suggestions for improvement across **style**, **functionality**, **security**.
* No code commits, only comments.

### Success Criteria

* AI comment appears automatically on PRs.
* Feedback is coherent, relevant, and useful.
* Runs within minutes and supports diffs up to a few thousand tokens.

### Tech Stack

* GitHub Actions
* Python (script to handle logic)
* OpenAI API (start with GPT-4)
* GitHub REST API (`GITHUB_TOKEN` for commenting)

### Secrets Needed

* `OPENAI_API_KEY` (or `ANTHROPIC_API_KEY`) in repo secrets.

### Timeline

* 1 day hackathon

* Morning: scaffold GitHub Action + Python script
* Afternoon: integrate LLM API + GitHub comment post
* End: test with sample PRs and tune prompt
