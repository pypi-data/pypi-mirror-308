import argparse
import asyncio
import os
from typing import Optional, List, Dict, Any
import aiohttp
import json
import zipfile
import tempfile
from pathlib import Path


async def process_stream(response: aiohttp.ClientResponse) -> List[Dict[str, Any]]:
    """Process the streaming response from the hackbot service."""
    results = []
    async for line in response.content:
        line = line.decode("utf-8")
        if line.startswith("data: "):
            try:
                json_str = line[5:].strip()  # Remove 'data: ' prefix
                print(f"{json_str}")  # Stream to stdout
                json_obj = json.loads(json_str)
                results.append(json_obj)
            except json.JSONDecodeError:
                print(f"Failed to parse JSON: {json_str}")
    return results


def compress_source_code(source_path: str, zip_path: str) -> None:
    """Compress the source code directory into a zip file."""
    try:
        with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zipf:
            for root, dirs, files in os.walk(source_path):
                # Skip hidden directories
                dirs[:] = [d for d in dirs if not d.startswith(".")]
                for file in files:
                    # Skip hidden files and .zip files
                    if not file.startswith(".") and not file.endswith(".zip"):
                        file_path = os.path.join(root, file)
                        arcname = os.path.relpath(file_path, source_path)
                        zipf.write(file_path, arcname)
    except Exception as e:
        raise RuntimeError(f"Failed to compress source code: {str(e)}")


async def hack_target(address: str, port: int, api_key: str, source_path: str = ".", output: Optional[str] = None) -> List[Dict[str, Any]]:
    """
    Analyze the target source code using the hackbot service.

    Args:
        address: The hackbot service address
        port: The service port number
        api_key: Authentication API key
        source_path: Path to the source code to analyze
        output: Optional path to save results

    Returns:
        List of analysis results
    """
    # Compress the source code into a tempfile
    with tempfile.NamedTemporaryFile(delete=True, suffix=".zip") as temp_zip:
        compress_source_code(source_path, temp_zip.name)

        url = f"{address}:{port}/api/hack"
        headers = {"X-API-KEY": api_key, "Connection": "keep-alive"}

        # Prepare the form data
        data = aiohttp.FormData()
        data.add_field("file", open(temp_zip.name, "rb"), filename="compressed_source_code.zip", content_type="application/zip")
        data.add_field("repo_url", "https://github.com/not_implemented")

        timeout = aiohttp.ClientTimeout(total=None)
        async with aiohttp.ClientSession(timeout=timeout) as session:
            async with session.post(url, data=data, headers=headers) as response:
                if response.status != 200:
                    raise RuntimeError(f"Hack request failed: {response.status}")

                results = await process_stream(response)

                # Save results if output path specified
                if output:
                    output_path = Path(output)
                    output_path.parent.mkdir(parents=True, exist_ok=True)
                    with open(output_path, "w") as f:
                        json.dump(results, f, indent=2)

                return results


async def authenticate(address: str, port: int, api_key: str) -> bool:
    """Verify API key authentication with the hackbot service."""
    url = f"{address}:{port}/api/authenticate"
    headers = {"X-API-KEY": api_key}

    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as response:
            return response.status == 200


async def generate_issues(issues_repo: str, github_api_key: str, results: List[Dict[str, Any]]) -> None:
    """
    Generate GitHub issues for bugs discovered by the bot.

    This function creates a master issue in the specified GitHub repository
    containing all the bugs found. It uses the GitHub API to create issues
    and requires appropriate authentication and permissions.

    Args:
        issues_repo (str): The full name of the GitHub repository (e.g., "owner/repo").
        github_api_key (str): The GitHub token for authentication.
        results (List[Dict[str, Any]]): A list of dictionaries containing bug information.

    Returns:
        None

    Raises:
        Exception: If there are permission issues or other errors when interacting with the GitHub API.

    Note:
        - This function requires a GitHub token with 'issues: write' and 'contents: read' permissions.
        - It creates a master issue with a title format of "HB-{number}".
    """
    auth = Auth.Token(github_api_key)
    g = Github(auth=auth)

    if not issues_repo:
        print("Error: GitHub repository is not specified.")
        return

    # Get a list of the bugs discovered by the bot
    issues_found = [issue for issue in results if issue.get("bug_id") is not None]
    if len(issues_found) == 0:
        print("No bugs found, skipping issue generation")
        return

    # Get the output repository. This will fail if the github token does not have access to the repository
    repo = None
    try:
        repo = g.get_repo(issues_repo)
    except GithubException as e:
        print(f"Error accessing repository: {e}")
        return

    last_hb_issue = 0
    # Fetch all existing issues in the repository and find the last one created by the bot
    for issue in repo.get_issues(state="all"):
        if issue.title.startswith("HB-"):
            last_hb_issue = int(issue.title.split("-")[1])
            break

    # Create a master issue in the repository that will contain all the bugs.
    # This will fail if the github token does not have write access to the issues
    # permissions:
    # - issues: write
    master_issue = None
    try:
        master_issue = repo.create_issue(title=f"HB-{last_hb_issue + 1}")
    except GithubException as e:
        print(f"Error creating issue: {e}")
        if e.status == 422:
            raise Exception("Validation failed, aborting. This functionality requires a GITHUB_TOKEN with 'issues: write' in the workflow permissions section.")
        elif e.status == 403:
            raise Exception("Forbidden, aborting. This functionality requires a GITHUB_TOKEN with 'issues: write' in the workflow permissions section.")
        elif e.status == 410:
            raise Exception("Gone, aborting. The repository does not allow issues.")

    # Add each bug as a comment to the master issue
    for issue in issues_found:
        body = f"#{issue.get('bug_id')} - {issue.get('bug_title')}\n{issue.get('bug_description')}"
        master_issue.create_comment(body=body)

    print(f"Created issue: {master_issue.title}")


def main() -> None:
    """CLI entrypoint for the hackbot tool."""
    parser = argparse.ArgumentParser(description="Hackbot - Eliminate bugs from your code")
    parser.add_argument("--address", default="https://app.hackbot.org", help="Hackbot service address (default: app.hackbot.org)")
    parser.add_argument("--port", type=int, default=443, help="Service port number (default: 80)")
    parser.add_argument("--api-key", required=True, help="API key for authentication")
    parser.add_argument("--source", required=True, help="Path to source code directory")
    parser.add_argument("--output", help="Path to save analysis results")
    parser.add_argument("--auth-only", action="store_true", help="Only verify API key authentication")

    issue_parser = parser.add_argument_group("Issue Generation Options")
    issue_parser.add_argument(
        "--issues_repo",
        type=str,
        help="The repository to generate issues in (format: username/repo). By default empty and so no issues are generated",
    )
    issue_parser.add_argument(
        "--github_api_key",
        type=str,
        required=False,
        help="GitHub API key for issue generation",
    )

    args = parser.parse_args()

    # Run the async operations
    try:
        # Verify authentication
        if not asyncio.run(authenticate(args.address, args.port, args.api_key)):
            print("Authentication failed")
            return 1

        print("Authentication successful")

        if args.auth_only:
            return 0

        # Perform the analysis
        results = asyncio.run(hack_target(args.address, args.port, args.api_key, args.source, args.output))

        if not results:
            print("No issues found")
        elif args.issues_repo:
            print("Generating issues")
            asyncio.run(generate_issues(args.issues_repo, args.github_api_key, results))
        else:
            print("No issues repo specified, so no issues will be generated")

        # Output results to output-path
        if args.output:
            with open(args.output, "w") as f:
                json.dump(results, f, indent=2)

        return 0

    except Exception as e:
        print(f"Error: {str(e)}")
        return 1


if __name__ == "__main__":
    exit(main())
