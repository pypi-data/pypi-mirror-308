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

        url = f"https://{address}:{port}/api/hack"
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
    url = f"https://{address}:{port}/api/authenticate"
    headers = {"X-API-KEY": api_key}

    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as response:
            return response.status == 200


def main() -> None:
    """CLI entrypoint for the hackbot tool."""
    parser = argparse.ArgumentParser(description="Hackbot - Eliminate bugs from your code")
    parser.add_argument("--address", default="app.hackbot.org", help="Hackbot service address (default: app.hackbot.org)")
    parser.add_argument("--port", type=int, default=443, help="Service port number (default: 80)")
    parser.add_argument("--api-key", required=True, help="API key for authentication")
    parser.add_argument("--source", required=True, help="Path to source code directory")
    parser.add_argument("--output", help="Path to save analysis results")
    parser.add_argument("--auth-only", action="store_true", help="Only verify API key authentication")

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

        return 0

    except Exception as e:
        print(f"Error: {str(e)}")
        return 1


if __name__ == "__main__":
    exit(main())
