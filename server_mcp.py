from datetime import datetime, time, timezone
from http import HTTPStatus
from json import JSONDecodeError
import sys
from mcp.server.fastmcp import FastMCP
import time as time_module

mcp = FastMCP("learning-mcp-server")

NOTES = {
    "today": "Learned MCP tool lifecycle: initialize -> list_tools -> call_tool.",
    "python": "Python FastMCP uses decorators like @mcp.tool and @mcp.resource.",
    "mcp": "Resources provide readable context; tools perform actions.",
}

@mcp.tool()
def get_time() -> dict:
    return {"now": datetime.now(timezone.utc).isoformat()}

@mcp.tool()
def sum_numbers(a: float, b: float) -> dict:
    return {"result": a + b}

@mcp.tool()
def multiply_numbers(a: float, b: float) -> dict:
    return {"result": a * b}

@mcp.resource("notes://today")
def today_notes() -> str:
    return NOTES["today"]

@mcp.resource("notes://python")
def python_notes() -> str:
    return NOTES["python"]

@mcp.resource("notes://mcp")
def mcp_note() -> str:
    return NOTES["mcp"]

@mcp.tool()
def get_note(title: str) -> dict:
    key = title.strip().lower()
    if key not in NOTES:
        raise ValueError(f"Note '{title}' not found")
    return {"title":key, "content":NOTES[key]}

@mcp.tool()
def get_http_json(url: str) -> dict:
    import httpx
    print(f"Fetching URL: {url}", file=sys.stderr, flush=True)
    response = httpx.get(url, timeout=8)
    response.raise_for_status()
    return {"status_code": response.status_code, "json": response.json()}

@mcp.tool()
def get_http_json_v2(url: str) -> dict:
    import httpx
    from urllib.parse import urlparse

    max_retry_count = 3
    total_attempts = max_retry_count + 1
    def fail(error_type: str, message: str) -> None:
        raise ValueError(f"[ERR] {error_type}: {message}")

    parsed = urlparse(url)
    if parsed.scheme not in {"http", "https"}:
        fail("invalid_url", "URL must start with http:// or https://")
    if not parsed.netloc:
        fail("invalid_url", "Invalid URL: missing host")
    for attempt in range(1, total_attempts + 1):
        try:
            response = httpx.get(url, timeout=8.0)
            response.raise_for_status()
            data = response.json()
            break  # success, exit retry loop
        except httpx.TimeoutException as e:
            if attempt < total_attempts:
                print(f"Request timed out for fetching URL: {url}, retrying now (Retry Attempt {attempt})", file=sys.stderr, flush=True)
                time_module.sleep(0.4)   # backoff, then retry
                continue
            else:
                fail("timeout", "Request timed out after 8 seconds")
        except httpx.HTTPStatusError as e:
            fail("http_status", f"HTTP {e.response.status_code} for {url}")
        except JSONDecodeError as e:
            fail("non_json", "Response body is not valid JSON")
        except httpx.RequestError as e:
            fail("network_error", str(e))
        except Exception as e:
            fail("unexpected", str(e))

    # Optional payload guard: avoid giant responses
    if isinstance(data, dict):
        preview = dict(list(data.items())[:20])  # first 20 keys
    elif isinstance(data, list):
        preview = data[:20]  # first 20 items
    else:
        preview = data

    res = f"[OK] {url}  Status={response.status_code}, Preview={preview}"
    return res

if __name__ == "__main__":
    try:
        mcp.run()
    except KeyboardInterrupt:
        print("Interrupted, shutting down.")
        sys.exit(0)
