# AI Pull Request Reviewer

An automated code review system that uses OpenAI's GPT-4 to analyze Python pull requests and provide actionable feedback on code quality, style, functionality, and security.

## Features

- 🤖 **Automated Reviews**: AI-powered code analysis triggered on every PR
- 📊 **Quality Ratings**: Letter grade (A-F) for overall code quality
- 🎯 **Multi-aspect Analysis**: Reviews style, functionality, and security
- ⚡ **Fast Feedback**: Reviews posted within minutes of PR creation
- 🔒 **Secure**: Uses GitHub's built-in secrets management

## Prerequisites

- A GitHub repository with Python code
- OpenAI API key (with GPT-4 access)
- GitHub Actions enabled on your repository

## Setup Instructions

### 1. Add Required Secrets

Navigate to your GitHub repository settings and add the following secret:

**Settings → Secrets and variables → Actions → New repository secret**

- **Name**: `OPENAI_API_KEY`
- **Value**: Your OpenAI API key

> **Note**: `GITHUB_TOKEN` is automatically provided by GitHub Actions.

### 2. Install the Workflow

The repository already contains the necessary files:

```
.github/workflows/pr-review.yml  # GitHub Actions workflow
review_pr.py                      # Main review script
requirements.txt                  # Python dependencies
```

If setting up in a new repository, copy these files to your repo and commit them to your default branch.

### 3. Test the Setup

Create a test pull request with Python file changes:

1. Create a new branch: `git checkout -b test-pr-review`
2. Make changes to a `.py` file (or create a new one)
3. Commit and push: `git add . && git commit -m "Test changes" && git push origin test-pr-review`
4. Open a pull request on GitHub
5. Watch the "Actions" tab for the workflow execution
6. The AI review comment should appear on the PR within a few minutes

## How It Works

1. **Trigger**: The workflow runs when a PR is opened, updated, or reopened (only if Python files are changed)
2. **Diff Extraction**: The script fetches the diff between the base and head commits
3. **AI Analysis**: The diff is sent to OpenAI GPT-4 with a structured review prompt
4. **Comment Posting**: The AI's review is posted as a comment on the PR

## Review Structure

Each AI review includes:

1. **Overall Code Quality Rating** - Letter grade (A-F)
2. **Style & Best Practices** - PEP 8, naming, documentation
3. **Functionality & Logic** - Correctness, edge cases, efficiency
4. **Security Concerns** - Vulnerabilities and unsafe operations
5. **Specific Recommendations** - Actionable improvements

## Configuration

### Adjusting the AI Model

Edit `review_pr.py` to change the model:

```python
model="gpt-4"  # Change to "gpt-4-turbo" or "gpt-3.5-turbo"
```

### Modifying the Review Prompt

The review prompt is in the `create_review_prompt()` method of `review_pr.py`. Customize it to focus on specific aspects or add domain-specific requirements.

### Changing Trigger Conditions

Edit `.github/workflows/pr-review.yml` to modify when the workflow runs:

```yaml
on:
  pull_request:
    types: [opened, synchronize, reopened]  # Add/remove event types
    paths:
      - '**.py'  # Add other file patterns if needed
```

## Limitations

- **Token Limits**: Very large diffs (>15,000 characters) are automatically truncated
- **Python Only**: Currently only reviews `.py` files (can be extended)
- **Rate Limits**: Subject to OpenAI API rate limits
- **Cost**: Each review consumes OpenAI API tokens (monitor your usage)

## Troubleshooting

### Workflow doesn't trigger
- Ensure the workflow file is in the default branch
- Check that Python files were modified in the PR
- Verify GitHub Actions are enabled for the repository

### Review comment not posted
- Check the Actions tab for error logs
- Verify `OPENAI_API_KEY` is set correctly
- Ensure the repository has "Read and write permissions" for workflows:
  - Settings → Actions → General → Workflow permissions

### OpenAI API errors
- Verify your API key is valid and has GPT-4 access
- Check your OpenAI account for sufficient credits
- Review rate limits on your OpenAI account

## Security Best Practices

- ✅ Never commit API keys to the repository
- ✅ Use GitHub Secrets for sensitive information
- ✅ Regularly rotate API keys
- ✅ Monitor OpenAI usage and costs
- ✅ Review the workflow permissions (principle of least privilege)

## Cost Estimation

- GPT-4 pricing: ~$0.03 per 1K input tokens, ~$0.06 per 1K output tokens
- Average review (2K input, 1K output): ~$0.12 per review
- Monitor your usage in the OpenAI dashboard

## Future Enhancements

Potential improvements for production use:
- Support for multiple programming languages
- Inline comments on specific code lines
- Integration with code quality metrics
- Customizable review severity levels
- Comparison with previous reviews
- Integration with other AI providers (Anthropic Claude, etc.)

## License

This project is provided as-is for hackathon and educational purposes.

## Support

For issues or questions:
1. Check the Actions tab for detailed logs
2. Review the troubleshooting section above
3. Consult OpenAI API documentation
4. Check GitHub Actions documentation

